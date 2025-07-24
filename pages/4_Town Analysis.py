import streamlit as st 
import requests
import urllib
import json
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
import time
import warnings

warnings.filterwarnings("ignore")

# display title and caption 
st.title("🏘️ Town Analysis")
st.caption("Filter to explore available units that match your needs!")

st.image("images/tengah.jpg", caption = "Tengah (For illustration purpose only)", use_container_width = False, width = 700)

# dropdown for user to select a month
month = st.selectbox("Select a month: ", 
                     ("2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", 
                      "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08"))

# dropdown for user to select a flat type 
flat_type = st.selectbox("Select a flat type: ", 
                         ("2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"))

# dropdown for user to select a town 
town = st.selectbox("Select a town", 
                    ('ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH','CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
                    'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON',
                    'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN'))

# set up API parameters 
dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
column_filters = ""
row_filters = {}
offset = None
sort = None
filters = {"month": f"{month}", "town": f"{town}", "flat_type": f"{flat_type}"}
for key, value in row_filters.items():
    filters[key] = {
        "type": "ILIKE",
        "value": str(value) if value is not None else ""
    }

row_filters_encoded = urllib.parse.quote(json.dumps(filters))

url = "https://data.gov.sg/api/action/datastore_search?resource_id=" + dataset_id
if column_filters:
  url = url + "&fields=" + column_filters
if filters:
  url = url + "&filters=" + row_filters_encoded
if offset:
  url = url + "&offset=" + offset
if sort:
  url = url + "&sort=" + sort

url += "&limit=10000"

response = requests.get(url)
data = response.json()

# convert JSON records into DataFrame and remove irrelevant columns 
df = pd.DataFrame(data['result']['records']).drop(columns = ['_id'], axis = 1)

# convert the resale price into integer
df['resale_price'] = df['resale_price'].astype(int)

min_price = df['resale_price'].min()
max_price = df['resale_price'].max()

# select slider for user to select the price range
price_range = st.select_slider("Select a resale price range (SGD)", 
                               options = list(range(min_price, max_price+1)),
                               value = (min_price, max_price))

df = df[(df['resale_price'] >= price_range[0]) & (df['resale_price'] <= price_range[1])]

# function to extract years from "remaining_lease" string 
def extract_remaining_lease_years(data):
  years = data.split("years")[0]
  return int(years)

# apply the function to create a new column for remaining lease in years 
df['remaining_lease_years'] = df['remaining_lease'].apply(extract_remaining_lease_years)

# function to convert the remaining lease years into categorical 
def convert_remaining_lease_years_to_cat(data):
  if data >= 0 and data <= 60:
    return "0 to 60 years"
  elif data >= 61 and data <= 80:
    return "61 to 80 years"
  elif data >= 81 and data <= 99:
    return "81 to 99 years"
  
# apply the function to create a column for remaining lease years into category
df['cat_remaining_lease_years'] = df['remaining_lease_years'].apply(convert_remaining_lease_years_to_cat)


# combine block and town to form the address string for geocoding 
df['address'] = df['block'] + ' ' + df['town']

# initialize the nomination geocoder with a user agent name 
geolocator = Nominatim(user_agent="hdb_locator")

# define function to get latitude and longitude from an address 
def get_coordinates(address):
    try:
        location = geolocator.geocode(address, timeout = 2)
        time.sleep(1)
        if location:
            return pd.Series([location.latitude, location.longitude])
    except:
        pass
    return pd.Series([None, None])

# apply the function to each address and store the results in latitude and longitude columns
df[['latitude', 'longitude']] = df['address'].apply(get_coordinates)

df = df.dropna(subset=['latitude', 'longitude'])

# create a base folium map centered in Singapore
m = folium.Map(location=[1.3521, 103.8198], zoom_start=12)

# add a marker for each resale flat on the map 
for i in range(len(df)):
    folium.Marker(
        location = [df.iloc[i]['latitude'], df.iloc[i]['longitude']],
        popup = ('BLK ' + df.iloc[i]['block'] + ', ' + df.iloc[i]['street_name'] + ', ' + df.iloc[i]['storey_range'] + ', Resale: $' + str(df.iloc[i]['resale_price']) + ', ' + str(df.iloc[i]['remaining_lease_years']) + ' years remaining'),
        tooltip = ('BLK ' + df.iloc[i]['block'] + ', ' + df.iloc[i]['street_name'] + ', ' + df.iloc[i]['storey_range'] + ', Resale: $' + str(df.iloc[i]['resale_price']) + ', ' + str(df.iloc[i]['remaining_lease_years']) + ' years remaining')
    ).add_to(m)
st_folium(m, width = 750)