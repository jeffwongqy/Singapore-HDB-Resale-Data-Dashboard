import streamlit as st 
import requests
import urllib
import json
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt

# display title and caption 
st.title("📊 Distribution of Resale Prices")
st.caption("Discover the estimated monthly median resale flat prices across different towns")

# display images
st.image("images/bishan.jpg", caption = "Bishan - Ang Mo Kio (For illustration purpose only)", use_container_width = False, width = 700)

# dropdown for user to select a month
month = st.selectbox("Select a month: ", 
                     ("2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06", "2024-07", "2024-08", "2024-09", "2024-10", "2024-11", "2024-12", 
                      "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06", "2025-07", "2025-08"))


# dropdown for user to select a flat type 
flat_type = st.selectbox("Select a flat type: ", 
                         ("2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"))

# dropdown for user to filter by remaining lease years category 
remaining_lease_years_cat = st.selectbox("Select remaining lease years: ", 
                                     ("0 to 60 years", "61 to 80 years", "81 to 99 years"))


# set up API parameters 
dataset_id = "d_8b84c4ee58e3cfc0ece0d773c8ca6abc"
column_filters = ""
row_filters = {}
offset = None
sort = None
filters = {"month": f"{month}", "flat_type": f"{flat_type}"}

# encode filters for URL 
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

# send GET request to the API
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

# filter data based on selected remaining lease years category 
if remaining_lease_years_cat == "0 to 60 years":
  df = df[(df['remaining_lease_years'] >= 0) & (df['remaining_lease_years'] <= 60)]
elif remaining_lease_years_cat == "61 to 80 years":
  df = df[(df['remaining_lease_years'] >= 61) & (df['remaining_lease_years'] <= 80)]
elif remaining_lease_years_cat == "81 to 99 years":
  df = df[(df['remaining_lease_years'] >= 81) & (df['remaining_lease_years'] <= 99)]

# compute median resale prices by town 
df_median_resale_prices = df.groupby('town')['resale_price'].median().reset_index()


# create scatterplot with annotations 
sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize = (20, 20))
sns.scatterplot(data = df_median_resale_prices, x = "resale_price", y = "town", hue = "town", ax = ax, s = 300)

for i, row in df_median_resale_prices.iterrows():
  ax.text(row['resale_price'], row['town'], row['town'] + ", $" + str(round(row['resale_price'], 2)), 
          fontsize = 18, 
          va = "center")

plt.title("Median Resale Price for {} as at {}".format(flat_type, month), fontsize = 30, fontweight = "bold")
plt.xlabel("Median Resale Price (SGD)", fontweight = "bold", fontsize = 30)
plt.ylabel("Town", fontweight = "bold", fontsize = 30)
plt.xticks(rotation = 45, fontsize = 20)
plt.yticks(fontsize = 20)
plt.tight_layout()
plt.legend().remove()
st.pyplot(fig)