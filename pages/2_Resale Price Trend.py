import streamlit as st
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns 

st.title("📈 Resale Price Trend")
st.caption("Monthly variation in median resale prices across towns")

st.image("images/toa_payoh.jpg", caption = "Toa Payoh (For illustration purpose only)", use_container_width = False, width = 700)

filepath = "/Users/jeffreywongqiyuan/Desktop/personal_projects/bto_resale_prices/dataset/resale_price.csv"

df = pd.read_csv(filepath)

df = df[(df['month'] >= "2024-01") & (df['month'] <= "2025-07")]


selected_town = st.multiselect("Select a town", 
                    ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT PANJANG', 'BUKIT TIMAH','CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI',
                    'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON',
                    'TAMPINES', 'TOA PAYOH', 'WOODLANDS', 'YISHUN'])

selected_flat_type = st.selectbox("Select a flat type: ", 
                         ("2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"))


df = df[df['town'].isin(selected_town)]

df['resale_price'] = df['resale_price'].astype(int)

df = df[df['flat_type'].isin([selected_flat_type])]

median_resale_price = df.groupby(['town', 'month'])['resale_price'].median().reset_index()

sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize = (15, 10))
sns.set_style("darkgrid")
sns.lineplot(x = "month", y = "resale_price", hue = "town", marker = "o", data = median_resale_price, ax = ax)
plt.title("Median Resale Price Trends Across Towns (2024-2025) \n for {}".format(selected_flat_type), fontsize = 30, fontweight = "bold")
plt.xlabel("Month", fontsize = 30, fontweight = "bold")
plt.ylabel("Resale Price", fontsize = 30, fontweight = "bold")
plt.xticks(rotation = 45, fontsize = 20)
plt.yticks(fontsize = 20)
plt.legend(bbox_to_anchor = (1.1, 0.5), loc = "center", fontsize = 11)
st.pyplot(fig)


