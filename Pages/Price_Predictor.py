import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor")

# Load files
with open('df.pkl', 'rb') as file:
    df = pickle.load(file)

with open('pipeline.pkl', 'rb') as file:
    pipeline = pickle.load(file)

st.header("Property Price Predictor")
st.subheader("Enter Property Details")

# Collect user input with correct types
# Inputs (align exactly with training column names)

property_type = st.selectbox('Property Type', sorted(df['property_type'].unique().tolist()))
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
bedroom = float(st.selectbox('Number of Bedrooms', sorted(df['bedRoom'].unique().tolist())))
bathroom = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox('Balconies', sorted(df['balcony'].unique().tolist()))
age_possession = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
built_up_area = float(st.number_input('Built-up Area (sq.ft)'))
servant_room = float(st.selectbox('Servant Room',[0.0,1.0]))
store_room = float(st.selectbox('Store Room',[0.0,1.0]))
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button("Predict"):
        data=[[property_type, sector, bedroom, bathroom, balcony, age_possession, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
        column = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']
        one_df = pd.DataFrame(data,columns=column)

        based_price = np.expm1(pipeline.predict(one_df))[0]
        st.text(f"Predicted Price: ₹{based_price:}")