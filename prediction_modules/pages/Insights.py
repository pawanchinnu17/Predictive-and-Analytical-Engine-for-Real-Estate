import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Data Insights", layout="wide")
st.title("Property Data Insights")

# Load data
data_file = 'data_viz1.csv'
df = pd.read_csv(data_file)

# Load sector feature highlights if available
try:
    feature_text = pickle.load(open('sector_feature_text.pkl', 'rb'))
except Exception:
    feature_text = None

st.header("Key Data Insights")

# 1. Price difference between property types
mean_price_house = df[df['property_type'] == 'house']['price'].mean()
mean_price_flat = df[df['property_type'] == 'flat']['price'].mean()
if not np.isnan(mean_price_house) and not np.isnan(mean_price_flat):
    diff = mean_price_house - mean_price_flat
    pct = 100 * diff / mean_price_flat
    st.markdown(f"**Houses are on average ₹{diff:,.2f} ({pct:.1f}%) more expensive than flats.")

# 2. Price per built-up area
corr_area_price = df['built_up_area'].corr(df['price'])
st.markdown(f"**There is a correlation of {corr_area_price:.2f} between built-up area and price.** Larger properties tend to be more expensive.")

# 3. Price by number of bedrooms
bedroom_price = df.groupby('bedRoom')['price'].mean().reset_index()
if not bedroom_price.empty:
    max_bed = int(bedroom_price['bedRoom'].max())
    min_bed = int(bedroom_price['bedRoom'].min())
    price_max_bed = bedroom_price[bedroom_price['bedRoom'] == max_bed]['price'].values[0]
    price_min_bed = bedroom_price[bedroom_price['bedRoom'] == min_bed]['price'].values[0]
    st.markdown(f"**Properties with {max_bed} bedrooms are on average ₹{price_max_bed:,.2f}, compared to ₹{price_min_bed:,.2f} for {min_bed} bedrooms.**")

# 4. Sector-level price differences
sector_price = df.groupby('sector')['price'].mean().sort_values(ascending=False)
top_sector = sector_price.index[0]
bottom_sector = sector_price.index[-1]
st.markdown(f"**The most expensive sector on average is {top_sector} (₹{sector_price.iloc[0]:,.2f}), while the least expensive is {bottom_sector} (₹{sector_price.iloc[-1]:,.2f}).**")

# 5. Price per sqft by property type
price_per_sqft_house = df[df['property_type'] == 'house']['price_per_sqft'].mean()
price_per_sqft_flat = df[df['property_type'] == 'flat']['price_per_sqft'].mean()
if not np.isnan(price_per_sqft_house) and not np.isnan(price_per_sqft_flat):
    st.markdown(f"**Houses have an average price per sqft of ₹{price_per_sqft_house:,.2f}, while flats have ₹{price_per_sqft_flat:,.2f}.**")

# 6. Feature highlights for a few sectors (if available)
if feature_text:
    st.subheader("Sector Feature Highlights")
    for sector in list(feature_text.keys())[:3]:
        st.markdown(f"**Sector {sector}:** {feature_text[sector][:200]}...")