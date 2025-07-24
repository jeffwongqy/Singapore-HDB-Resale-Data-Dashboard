import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("🏠 Welcome to the HDB Resale Price Explorer")
st.caption("Interactive Web Application for Visualizing and Analyzing HDB Resale Prices in Singapore")
st.sidebar.success("Choose one above to explore!")

st.image("images/tampines.jpg", caption = "Tampines (For illustration purpose only)", use_container_width = False, width = 700)

st.markdown(
    """
    Explore insightful trends and patterns in HDB resale prices using this interactive dashboard. Whether you're a homebuyer, researcher, or policymaker, 
    this tool helps you uncover key factors that influence resale prices across Singapore's towns.

    ### 🔍 What you can explore:
    1. 📊 **Distribution of Resale Prices:** Visualize the distribution of median resale flat prices across towns and flat types to identify price ranges and outliers.

    2. 📈 **Resale Price Trend:** Track how median resale prices change over time across different towns and flat types.

    3. 🏘️ **Town Analysis:** Filter by town, flat type, and other criteria to explore available units that meet your preferences.

    4. 📉 **Impact of Lease Years on Resale Prices:** Understand how the remaining lease duration affects the resale value of HDB flats across the island.

    """
)

