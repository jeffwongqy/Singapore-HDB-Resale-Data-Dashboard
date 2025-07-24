import streamlit as st 
import requests
import urllib
import json
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt

# display title and caption 
st.title("📉 Impact of Lease Years on Resale Prices")
st.caption("Discover the relationship between remaining lease duration and resale flat prices across Singapore")

# display images
st.image("images/jurong.jpg", caption = "Jurong (For illustration purpose only)", use_container_width = False, width = 700)

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


# create scatterplot with annotations
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize = (20, 20))
sns.scatterplot(data = df, x = "remaining_lease_years", y = "resale_price", hue = "cat_remaining_lease_years", ax = ax, s = 300)
plt.title("Resale Price for {} at {} as at {}".format(flat_type, town, month), fontsize = 30, fontweight = "bold")
plt.xlabel("Remaining Lease Years", fontweight = "bold", fontsize = 30)
plt.ylabel("Resale Price (SGD)", fontweight = "bold", fontsize = 30)
plt.xticks(rotation = 45, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.legend(fontsize = 20)
st.pyplot(fig)