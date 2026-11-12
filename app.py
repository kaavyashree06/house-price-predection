
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="HousePredict AI",
    page_icon="🏠",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}
[data-testid="stSidebar"] {
    background: #14213d;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg,#14213d,#315c91);
    padding: 35px;
    border-radius: 16px;
    color: white;
}
.hero h1, .hero p {
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

try:
    model = load_model()
except Exception:
    st.error("Unable to load the prediction service. Please try again later.")
    st.stop()

FEATURES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude"
]

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.title("🏠 HousePredict AI")
st.sidebar.caption("PROPERTY VALUE ESTIMATOR")
st.sidebar.divider()

page = st.sidebar.radio(
    "MENU",
    [
        "Dashboard",
        "Price Prediction",
        "Compare Properties",
        "Analytics",
        "My History"
    ]
)

st.sidebar.divider()
st.sidebar.caption("Your property assistant")

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to HousePredict AI 🏠</h1>
        <p>Discover the estimated value of your property
        in just a few seconds.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    a, b, c = st.columns(3)

    a.metric("Predictions Made", len(st.session_state.history))
    b.metric("Services", "4")
    c.metric("Status", "Online")

    st.divider()

    st.subheader("What would you like to do?")

    x, y = st.columns(2)

    with x:
        with st.container(border=True):
            st.subheader("🏡 Predict Property Price")
            st.write("Enter property details to get an estimated value.")
            if st.button("Predict Now", use_container_width=True):
                st.session_state.next_page = "Price Prediction"
                st.rerun()

    with y:
        with st.container(border=True):
            st.subheader("⚖️ Compare Properties")
            st.write("Compare the estimated values of two properties.")
            if st.button("Compare Now", use_container_width=True):
                st.session_state.next_page = "Compare Properties"
                st.rerun()

    if "next_page" in st.session_state:
        st.sidebar.info("Select your chosen page from the menu.")

elif page == "Price Prediction":

    st.title("🏡 Property Price Prediction")
    st.write("Enter the property information below.")

    with st.form("prediction_form"):

        left, right = st.columns(2)

        with left:
            income = st.number_input("Median Income", 0.0, 20.0, 5.0)
            age = st.number_input("House Age", 1.0, 100.0, 20.0)
            rooms = st.number_input("Average Rooms", 1.0, 20.0, 5.0)
            bedrooms = st.number_input("Average Bedrooms", 0.0, 10.0, 1.0)

        with right:
            population = st.number_input("Population", 1.0, 50000.0, 1000.0)
            occupancy = st.number_input("Average Occupancy", 1.0, 20.0, 3.0)
            latitude = st.number_input("Latitude", 32.0, 42.0, 34.0)
            longitude = st.number_input("Longitude", -125.0, -114.0, -118.0)

        submitted = st.form_submit_button(
            "Predict House Price",
            type="primary",
            use_container_width=True
        )

    if submitted:

        data = pd.DataFrame([[
            income, age, rooms, bedrooms,
            population, occupancy, latitude, longitude
        ]], columns=FEATURES)

        prediction = float(model.predict(data)[0])
        price = prediction * 100000

        st.session_state.history.append({
            "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Estimated Price (USD)": round(price, 2)
        })

        st.divider()
        st.success("Your property estimate is ready!")

        st.metric("Estimated Property Value", f"${price:,.2f}")

        st.caption("This is an estimated value, not a guaranteed selling price.")

elif page == "Compare Properties":

    st.title("⚖️ Compare Properties")
    st.write("Enter details for two properties.")

    properties = []

    for n in [1, 2]:

        st.subheader(f"Property {n}")

        a, b = st.columns(2)

        with a:
            income = st.number_input(f"Median Income {n}", 0.0, 20.0, 5.0, key=f"i{n}")
            age = st.number_input(f"House Age {n}", 1.0, 100.0, 20.0, key=f"a{n}")
            rooms = st.number_input(f"Average Rooms {n}", 1.0, 20.0, 5.0, key=f"r{n}")
            bedrooms = st.number_input(f"Average Bedrooms {n}", 0.0, 10.0, 1.0, key=f"b{n}")

        with b:
            population = st.number_input(f"Population {n}", 1.0, 50000.0, 1000.0, key=f"p{n}")
            occupancy = st.number_input(f"Average Occupancy {n}", 1.0, 20.0, 3.0, key=f"o{n}")
            latitude = st.number_input(f"Latitude {n}", 32.0, 42.0, 34.0, key=f"la{n}")
            longitude = st.number_input(f"Longitude {n}", -125.0, -114.0, -118.0, key=f"lo{n}")

        properties.append([
            income, age, rooms, bedrooms,
            population, occupancy, latitude, longitude
        ])

    if st.button("Compare Properties", type="primary"):

        results = model.predict(
            pd.DataFrame(properties, columns=FEATURES)
        ) * 100000

        a, b = st.columns(2)
        a.metric("Property 1", f"${results[0]:,.2f}")
        b.metric("Property 2", f"${results[1]:,.2f}")

        st.info(f"Price difference: ${abs(results[0]-results[1]):,.2f}")

elif page == "Analytics":

    st.title("📊 Property Analytics")

    if not st.session_state.history:
        st.info("Make your first prediction to see analytics.")
    else:
        history = pd.DataFrame(st.session_state.history)

        st.metric("Total Predictions", len(history))

        st.subheader("Prediction History")
        st.dataframe(history, use_container_width=True)

        st.subheader("Estimated Price Trends")
        st.line_chart(
            history.set_index("Date")["Estimated Price (USD)"]
        )

elif page == "My History":

    st.title("🕒 My Prediction History")

    if not st.session_state.history:
        st.info("No previous predictions available.")
    else:
        history = pd.DataFrame(st.session_state.history)

        st.dataframe(history, use_container_width=True)

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download History",
            csv,
            "my_property_history.csv",
            "text/csv"
        )

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

st.sidebar.divider()
st.sidebar.caption("HousePredict AI")
