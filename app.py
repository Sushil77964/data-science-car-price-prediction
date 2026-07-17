import streamlit as st
import pickle
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")

# Title
st.title("🚗 Car Price Prediction App")
st.write("Enter the car details below to predict the selling price.")

# Load Model
with open("models/random_forest_car_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# User Inputs
present_price = st.number_input("Present Price (Lakhs)", min_value=0.0, value=5.0)

kms_driven = st.number_input("Kilometers Driven", min_value=0, value=10000)

owner = st.selectbox("Owner", [0, 1, 2, 3])

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel"])

seller = st.selectbox("Seller Type", ["Dealer", "Individual"])

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

# Predict Button
if st.button("Predict Price"):

    input_data = pd.DataFrame({
        "Present_Price": [present_price],
        "Driven_kms": [kms_driven],
        "Owner": [owner],
        "Fuel_Type_Diesel": [1 if fuel == "Diesel" else 0],
        "Seller_Type_Individual": [1 if seller == "Individual" else 0],
        "Transmission_Manual": [1 if transmission == "Manual" else 0]
    })

    st.subheader("Input Data")
    st.dataframe(input_data)

    try:
        prediction = model.predict(input_data)
        st.success(f"💰 Estimated Selling Price: ₹ {prediction[0]:.2f} Lakhs")
    except Exception as e:
        st.error("Prediction Error")
        st.code(str(e))