
import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="House Price Prediction | SRM",
    page_icon="🏠",
    layout="wide"
)

@st.cache_resource
def load_model():
    return joblib.load("house_price_model.pkl")

model = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar navigation
st.sidebar.title("🏠 HousePredict AI")
st.sidebar.caption("Machine Learning Project")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "Price Prediction",
        "Model Insights",
        "Analytics",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.success("Machine Learning Model Loaded")
st.sidebar.caption("Algorithm: Random Forest Regressor")

# HOME PAGE
if page == "Home":

    st.title("🏠 House Price Prediction System")
    st.subheader("Intelligent Real Estate Price Estimation")
    st.write(
        "A machine learning application that estimates "
        "house prices using property and location information."
    )

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric("ML Algorithm", "Random Forest")
    c2.metric("Application", "Web Based")
    c3.metric("Dataset", "California Housing")

    st.divider()

    st.header("Welcome to HousePredict AI")

    st.write("""
    This project uses supervised machine learning to predict
    the estimated value of a house based on important
    property characteristics.

    The system accepts housing information, processes the
    input and generates a predicted house value using a
    trained Random Forest Regression model.
    """)

    st.subheader("Project Features")

    a, b = st.columns(2)

    with a:
        st.markdown("""
        - Interactive price prediction
        - Machine learning integration
        - Feature importance analysis
        """)

    with b:
        st.markdown("""
        - Prediction history
        - Data visualization
        - User-friendly interface
        """)

    if st.button("Start Price Prediction"):
        st.session_state.current_page = "Price Prediction"
        st.rerun()

# PREDICTION PAGE
elif page == "Price Prediction":

    st.title("💰 House Price Prediction")
    st.write("Enter the property details below.")

    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        with col1:
            medinc = st.number_input(
                "Median Income",
                min_value=0.0,
                max_value=20.0,
                value=5.0
            )

            age = st.number_input(
                "House Age",
                min_value=1.0,
                max_value=100.0,
                value=20.0
            )

            rooms = st.number_input(
                "Average Rooms",
                min_value=1.0,
                max_value=20.0,
                value=5.0
            )

            bedrooms = st.number_input(
                "Average Bedrooms",
                min_value=0.0,
                max_value=10.0,
                value=1.0
            )

        with col2:
            population = st.number_input(
                "Population",
                min_value=1.0,
                max_value=50000.0,
                value=1000.0
            )

            occupancy = st.number_input(
                "Average Occupancy",
                min_value=1.0,
                max_value=20.0,
                value=3.0
            )

            latitude = st.number_input(
                "Latitude",
                min_value=32.0,
                max_value=42.0,
                value=34.0
            )

            longitude = st.number_input(
                "Longitude",
                min_value=-125.0,
                max_value=-114.0,
                value=-118.0
            )

        submitted = st.form_submit_button(
            "🔍 Predict House Price",
            use_container_width=True
        )

    if submitted:

        data = pd.DataFrame([[
            medinc, age, rooms, bedrooms,
            population, occupancy, latitude, longitude
        ]], columns=[
            "MedInc", "HouseAge", "AveRooms", "AveBedrms",
            "Population", "AveOccup", "Latitude", "Longitude"
        ])

        prediction = float(model.predict(data)[0])
        price = prediction * 100000

        st.session_state.history.append({
            "Time": datetime.now().strftime("%d-%m-%Y %H:%M"),
            "Predicted Price (USD)": round(price, 2)
        })

        st.divider()
        st.subheader("Prediction Result")

        st.success(
            f"Estimated House Value: ${price:,.2f}"
        )

        st.caption(
            "The prediction is an estimate based on the "
            "California Housing dataset and is not a real "
            "property valuation."
        )

# MODEL INSIGHTS PAGE
elif page == "Model Insights":

    st.title("📊 Machine Learning Model Insights")

    st.write(
        "This application uses a Random Forest Regressor "
        "trained on the California Housing dataset."
    )

    st.subheader("Algorithm Overview")

    st.write("""
    Random Forest is an ensemble learning algorithm.
    It combines predictions from multiple decision trees
    to produce a regression result.

    The model learns relationships between housing
    characteristics and their target values.
    """)

    st.subheader("Feature Importance")

    if hasattr(model, "feature_importances_"):

        features = [
            "Median Income",
            "House Age",
            "Average Rooms",
            "Average Bedrooms",
            "Population",
            "Average Occupancy",
            "Latitude",
            "Longitude"
        ]

        importance = model.feature_importances_

        chart_data = pd.DataFrame({
            "Feature": features,
            "Importance": importance
        }).sort_values("Importance", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 5))

        ax.barh(
            chart_data["Feature"],
            chart_data["Importance"]
        )

        ax.set_xlabel("Importance Score")
        ax.set_title("Random Forest Feature Importance")

        st.pyplot(fig)

        plt.close(fig)

    st.subheader("Model Information")

    st.write("""
    - Learning type: Supervised Learning
    - Problem type: Regression
    - Algorithm: Random Forest Regressor
    - Output: Predicted house value
    """)

# ANALYTICS PAGE
elif page == "Analytics":

    st.title("📈 Prediction Analytics")

    if len(st.session_state.history) == 0:

        st.info(
            "No predictions yet. Visit the Price Prediction "
            "page and make your first prediction."
        )

    else:

        history = pd.DataFrame(st.session_state.history)

        st.metric(
            "Total Predictions",
            len(history)
        )

        st.subheader("Prediction History")

        st.dataframe(
            history,
            use_container_width=True
        )

        st.subheader("Predicted Price Trend")

        st.line_chart(
            history.set_index("Time")["Predicted Price (USD)"]
        )

        csv = history.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Prediction History",
            csv,
            "prediction_history.csv",
            "text/csv"
        )

        if st.button("Clear Prediction History"):
            st.session_state.history = []
            st.rerun()

# ABOUT PROJECT PAGE
elif page == "About Project":

    st.title("📚 About the Project")

    st.subheader("Project Title")

    st.write(
        "House Price Prediction Using Machine Learning"
    )

    st.subheader("Problem Statement")

    st.write("""
    Estimating house prices accurately can be challenging
    because property values depend on several factors.

    This project develops a machine learning system that
    predicts estimated housing values using property,
    demographic and geographical features.
    """)

    st.subheader("Objectives")

    st.markdown("""
    1. Study and preprocess housing data.
    2. Apply machine learning regression techniques.
    3. Train a Random Forest prediction model.
    4. Evaluate model performance.
    5. Develop an interactive web application.
    """)

    st.subheader("Methodology")

    st.markdown("""
    **Step 1:** Dataset Collection

    **Step 2:** Data Preprocessing

    **Step 3:** Exploratory Data Analysis

    **Step 4:** Train-Test Splitting

    **Step 5:** Model Training

    **Step 6:** Model Evaluation

    **Step 7:** Web Application Development
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

    st.subheader("Dataset Information")

    st.write("""
    The project uses the California Housing dataset
    available through Scikit-learn.

    The target variable is Median House Value.
    Values are represented in units of $100,000.
    """)

    st.warning("""
    This project is trained on California housing data.
    It should not be used to estimate actual Indian
    property prices without training on suitable Indian
    housing data.
    """)

st.sidebar.divider()
st.sidebar.caption("SRM University | ML Main Project")
