import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Car Price Prediction", page_icon="🚗")

st.title("🚗 Car Price Prediction")
st.write("Enter car details below.")

# Load Model
with open("models/random_forest_car_price_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load Training Columns
with open("models/model_columns.pkl", "rb") as file:
    model_columns = pickle.load(file)

# Inputs
car_name = st.selectbox(
    "Car Name",
    [
        "ritz", "sx4", "ciaz", "wagon r", "swift",
        "vitara brezza", "alto 800", "baleno",
        "city", "corolla altis"
    ]
)

year = st.number_input("Year", 2000, 2025, 2018)

present_price = st.number_input("Present Price (Lakhs)", 0.0, 100.0, 5.0)

kms_driven = st.number_input("Kilometers Driven", 0, 500000, 25000)

owner = st.selectbox("Owner", [0, 1, 2, 3])

fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel"])

seller = st.selectbox("Seller Type", ["Dealer", "Individual"])

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

if st.button("Predict Price"):

    # Create all training columns with 0
    input_data = pd.DataFrame([[0] * len(model_columns)], columns=model_columns)

    # Fill numerical values
    input_data["Year"] = year
    input_data["Present_Price"] = present_price
    input_data["Driven_kms"] = kms_driven
    input_data["Owner"] = owner

    # One-hot encoding
    if "Fuel_Type_Diesel" in input_data.columns and fuel == "Diesel":
        input_data["Fuel_Type_Diesel"] = 1

    if "Selling_type_Individual" in input_data.columns and seller == "Individual":
        input_data["Selling_type_Individual"] = 1

    if "Transmission_Manual" in input_data.columns and transmission == "Manual":
        input_data["Transmission_Manual"] = 1

    car_column = "Car_Name_" + car_name

    if car_column in input_data.columns:
        input_data[car_column] = 1

    prediction = model.predict(input_data)

    st.success(f"💰 Estimated Selling Price: ₹ {prediction[0]:.2f} Lakhs")