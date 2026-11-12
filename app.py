
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os
from datetime import datetime

st.set_page_config(
    page_title="HousePredict AI",
    page_icon="🏠",
    layout="wide"
)

# Professional styling
st.markdown("""
<style>
.main {
    background-color: #f5f7fb;
}
[data-testid="stSidebar"] {
    background-color: #14213d;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
.hero {
    padding: 30px;
    border-radius: 16px;
    background: linear-gradient(120deg,#14213d,#315c91);
    color: white;
}
.hero h1, .hero p {
    color: white;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e4e9f2;
}
</style>
""", unsafe_allow_html=True)

# Load existing model
@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error("Could not load the machine learning model.")
    st.code(str(e))
    st.stop()

FEATURES = [
    "MedInc", "HouseAge", "AveRooms", "AveBedrms",
    "Population", "AveOccup", "Latitude", "Longitude"
]

FEATURE_NAMES = [
    "Median Income", "House Age", "Average Rooms",
    "Average Bedrooms", "Population",
    "Average Occupancy", "Latitude", "Longitude"
]

if "history" not in st.session_state:
    st.session_state.history = []

if "saved_properties" not in st.session_state:
    st.session_state.saved_properties = []

# Sidebar
st.sidebar.title("🏠 HousePredict AI")
st.sidebar.caption("SMART REAL ESTATE ANALYTICS")
st.sidebar.divider()

page = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Price Prediction",
        "Property Comparison",
        "Prediction History",
        "Model Insights",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.success("ML Model: Connected")
st.sidebar.caption("Random Forest Regressor")
st.sidebar.caption("SRM University | Main Project")

# Dashboard
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>HousePredict AI 🏠</h1>
        <p>Intelligent House Price Prediction Platform</p>
        <p>Predict. Analyse. Make smarter property decisions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3 = st.columns(3)

    c1.metric("ML Algorithm", "Random Forest")
    c2.metric("Model Status", "Active")
    c3.metric(
        "Total Predictions",
        len(st.session_state.history)
    )

    st.divider()

    st.subheader("Welcome to HousePredict AI")

    st.write("""
    HousePredict AI is a machine learning-based house
    price estimation application. It analyses property,
    demographic and geographical information to estimate
    housing values.

    The application uses a trained Random Forest
    Regression model and provides an interactive
    prediction and analytics experience.
    """)

    a, b = st.columns(2)

    with a:
        st.subheader("What you can do")
        st.markdown("""
        - Predict estimated house values
        - Compare two properties
        - Review prediction history
        - Explore machine learning insights
        """)

    with b:
        st.subheader("Technology")
        st.markdown("""
        - Python
        - Scikit-learn
        - Pandas
        - Matplotlib
        - Streamlit
        - Joblib
        """)

    if st.button("Start Predicting", type="primary"):
        st.session_state.go_prediction = True
        st.rerun()

# Prediction
elif page == "Price Prediction":

    st.title("💰 House Price Prediction")
    st.write("Enter the property details to estimate its value.")

    with st.form("house_form"):

        st.subheader("Property Information")

        c1, c2 = st.columns(2)

        with c1:
            medinc = st.number_input(
                "Median Income",
                0.0, 20.0, 5.0
            )
            age = st.number_input(
                "House Age",
                1.0, 100.0, 20.0
            )
            rooms = st.number_input(
                "Average Rooms",
                1.0, 20.0, 5.0
            )
            bedrooms = st.number_input(
                "Average Bedrooms",
                0.0, 10.0, 1.0
            )

        with c2:
            population = st.number_input(
                "Population",
                1.0, 50000.0, 1000.0
            )
            occupancy = st.number_input(
                "Average Occupancy",
                1.0, 20.0, 3.0
            )
            latitude = st.number_input(
                "Latitude",
                32.0, 42.0, 34.0
            )
            longitude = st.number_input(
                "Longitude",
                -125.0, -114.0, -118.0
            )

        submitted = st.form_submit_button(
            "🔍 Predict House Price",
            type="primary",
            use_container_width=True
        )

    if submitted:

        data = pd.DataFrame([[
            medinc, age, rooms, bedrooms,
            population, occupancy, latitude, longitude
        ]], columns=FEATURES)

        prediction = float(model.predict(data)[0])
        price = prediction * 100000

        record = {
            "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Median Income": medinc,
            "House Age": age,
            "Average Rooms": rooms,
            "Average Bedrooms": bedrooms,
            "Population": population,
            "Average Occupancy": occupancy,
            "Latitude": latitude,
            "Longitude": longitude,
            "Estimated Price (USD)": round(price, 2)
        }

        st.session_state.history.append(record)

        st.divider()
        st.subheader("Prediction Result")

        st.success("Prediction completed successfully!")

        st.metric(
            "Estimated House Value",
            f"${price:,.2f}"
        )

        st.info(
            "This is an estimate from the California Housing "
            "dataset, not a real property valuation."
        )

        with st.expander("View submitted property details"):
            st.dataframe(data, use_container_width=True)

# Property Comparison
elif page == "Property Comparison":

    st.title("🏘️ Property Comparison")
    st.write("Compare the estimated prices of two properties.")

    properties = []

    for number in [1, 2]:
        st.subheader(f"Property {number}")

        c1, c2 = st.columns(2)

        with c1:
            income = st.number_input(
                f"Median Income {number}",
                0.0, 20.0, 5.0,
                key=f"income{number}"
            )
            age = st.number_input(
                f"House Age {number}",
                1.0, 100.0, 20.0,
                key=f"age{number}"
            )
            rooms = st.number_input(
                f"Average Rooms {number}",
                1.0, 20.0, 5.0,
                key=f"rooms{number}"
            )
            bedrooms = st.number_input(
                f"Average Bedrooms {number}",
                0.0, 10.0, 1.0,
                key=f"bedrooms{number}"
            )

        with c2:
            population = st.number_input(
                f"Population {number}",
                1.0, 50000.0, 1000.0,
                key=f"population{number}"
            )
            occupancy = st.number_input(
                f"Average Occupancy {number}",
                1.0, 20.0, 3.0,
                key=f"occupancy{number}"
            )
            latitude = st.number_input(
                f"Latitude {number}",
                32.0, 42.0, 34.0,
                key=f"latitude{number}"
            )
            longitude = st.number_input(
                f"Longitude {number}",
                -125.0, -114.0, -118.0,
                key=f"longitude{number}"
            )

        properties.append([
            income, age, rooms, bedrooms,
            population, occupancy, latitude, longitude
        ])

    if st.button("Compare Properties", type="primary"):

        results = model.predict(
            pd.DataFrame(properties, columns=FEATURES)
        ) * 100000

        x, y = st.columns(2)

        x.metric("Property 1", f"${results[0]:,.2f}")
        y.metric("Property 2", f"${results[1]:,.2f}")

        difference = abs(results[0] - results[1])

        st.info(
            f"Difference in estimated values: ${difference:,.2f}"
        )

# History
elif page == "Prediction History":

    st.title("📋 Prediction History")

    if not st.session_state.history:
        st.info("No predictions yet. Make a prediction first.")

    else:
        history = pd.DataFrame(st.session_state.history)

        st.metric(
            "Total Predictions",
            len(history)
        )

        st.dataframe(
            history,
            use_container_width=True
        )

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Prediction Report",
            csv,
            "house_prediction_history.csv",
            "text/csv"
        )

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    st.caption(
        "History is stored for the current application session."
    )

# Model Insights
elif page == "Model Insights":

    st.title("📊 Machine Learning Insights")

    st.subheader("Random Forest Regression")

    st.write("""
    Random Forest is an ensemble machine learning
    algorithm. It combines multiple decision trees
    to produce a regression prediction.

    This project uses the algorithm to estimate
    median house values.
    """)

    if hasattr(model, "feature_importances_"):

        st.subheader("Feature Importance")

        importance = model.feature_importances_

        chart = pd.DataFrame({
            "Feature": FEATURE_NAMES,
            "Importance": importance
        }).sort_values("Importance")

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.barh(
            chart["Feature"],
            chart["Importance"]
        )

        ax.set_xlabel("Importance Score")
        ax.set_title("Random Forest Feature Importance")

        st.pyplot(fig)
        plt.close(fig)

        st.write(
            "Feature importance indicates how much each "
            "feature contributes to the model's decisions."
        )

    st.subheader("Model Configuration")

    st.write(f"Number of trees: {getattr(model, 'n_estimators', 'Not available')}")
    st.write(f"Maximum tree depth: {getattr(model, 'max_depth', 'Not available')}")
    st.write("Learning type: Supervised Learning")
    st.write("Problem type: Regression")

    st.warning(
        "Actual R², MAE and RMSE scores should be taken "
        "from the model evaluation performed in Google Colab."
    )

# About
elif page == "About Project":

    st.title("📚 About HousePredict AI")

    st.subheader("Project Abstract")

    st.write("""
    HousePredict AI is a machine learning-based application
    developed to estimate house values using housing data.

    It uses a Random Forest Regression model trained on
    the California Housing dataset. The application
    provides a web interface for predictions, comparison
    and visualization of model insights.
    """)

    st.subheader("Problem Statement")

    st.write("""
    House prices depend on several factors, including
    income, property characteristics and geographical
    location. This project applies machine learning
    techniques to estimate house values from these features.
    """)

    st.subheader("Objectives")

    st.markdown("""
    1. Collect and understand housing data.
    2. Perform data preprocessing.
    3. Explore housing data through visualizations.
    4. Train a Random Forest regression model.
    5. Evaluate model performance.
    6. Develop an interactive prediction application.
    """)

    st.subheader("Project Workflow")

    st.markdown("""
    Dataset Collection → Data Cleaning → Data Analysis
    → Train-Test Split → Model Training → Evaluation
    → Web Application Deployment
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - Python
    - Pandas and NumPy
    - Scikit-learn
    - Matplotlib
    - Streamlit
    - Joblib
    - Google Colab
    - GitHub
    """)

    st.subheader("Dataset")

    st.write("""
    California Housing dataset from Scikit-learn.
    It contains 20,640 observations and 8 input features.
    The target is median house value, expressed in
    units of $100,000.
    """)

    st.warning(
        "This application is a California housing "
        "prediction demonstration. It does not estimate "
        "Indian property market prices."
    )

st.sidebar.divider()
st.sidebar.caption("HousePredict AI | SRM Main Project")
