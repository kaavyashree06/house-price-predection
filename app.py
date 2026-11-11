import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="House Price Prediction", page_icon="🏠")

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

st.title("🏠 House Price Prediction")
st.write("Enter house details to predict its price.")

medinc = st.number_input("Median Income", 0.0, 20.0, 5.0)
age = st.number_input("House Age", 1.0, 100.0, 20.0)
rooms = st.number_input("Average Rooms", 1.0, 20.0, 5.0)
bedrooms = st.number_input("Average Bedrooms", 0.0, 10.0, 1.0)
population = st.number_input("Population", 1.0, 50000.0, 1000.0)
occupancy = st.number_input("Average Occupancy", 1.0, 20.0, 3.0)
latitude = st.number_input("Latitude", 32.0, 42.0, 34.0)
longitude = st.number_input("Longitude", -125.0, -114.0, -118.0)

if st.button("Predict House Price"):
    data = pd.DataFrame([[
        medinc, age, rooms, bedrooms,
        population, occupancy, latitude, longitude
    ]], columns=[
        "MedInc", "HouseAge", "AveRooms", "AveBedrms",
        "Population", "AveOccup", "Latitude", "Longitude"
    ])

    prediction = model.predict(data)[0] * 100000
    st.success(f"Estimated House Price: ${prediction:,.2f}")
