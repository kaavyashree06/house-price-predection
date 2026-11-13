
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Haven | House Price Prediction",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

@st.cache_resource
def load_model():
    model_path = Path(__file__).parent / "house_price_model.pkl"
    return joblib.load(model_path)

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    model = None
    model_loaded = False

# ==========================================
# SESSION HISTORY
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# GLASSMORPHISM DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255,255,255,0.85), transparent 35%),
        linear-gradient(135deg, #f4e9dc, #dfc7ad, #efe1d0);
    color: #493629;
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3, h4 {
    color: #493629 !important;
    font-weight: 700 !important;
}

p, label {
    color: #604a38;
}

section[data-testid="stSidebar"] {
    background: rgba(255,248,239,0.75);
    backdrop-filter: blur(25px);
    border-right: 1px solid rgba(255,255,255,0.8);
}

section[data-testid="stSidebar"] * {
    color: #513d2e;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(80,50,25,0.08);
}

div[data-testid="stMetricLabel"] {
    color: #82674f !important;
}

div[data-testid="stMetricValue"] {
    color: #493629 !important;
    font-weight: 700;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,250,244,0.5);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(91,61,36,0.08);
    padding: 12px;
}

.stButton > button {
    background: linear-gradient(135deg, #9c7654, #694a32);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #765338, #4e3524);
    transform: translateY(-2px);
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: rgba(255,255,255,0.7) !important;
    color: #493629 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,0.7);
    border-radius: 10px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(255,255,255,0.3);
    padding: 8px;
    border-radius: 14px;
}

.stTabs [aria-selected="true"] {
    background: rgba(255,255,255,0.8);
    color: #493629 !important;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

hr {
    border-color: rgba(105,74,50,0.18);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

.main .block-container {
    animation: fadeIn 0.5s ease-in-out;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# COMMON FUNCTIONS
# ==========================================

FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
]

def predict_price(values):
    data = pd.DataFrame([values], columns=FEATURES)
    prediction = float(model.predict(data)[0])
    return max(0, prediction * 100000)

def property_inputs(prefix):
    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Median Income (in $10,000s)",
            min_value=0.5,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key=f"{prefix}_income"
        )

        age = st.number_input(
            "House Age (years)",
            min_value=1,
            max_value=100,
            value=25,
            key=f"{prefix}_age"
        )

        rooms = st.number_input(
            "Average Rooms",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key=f"{prefix}_rooms"
        )

        bedrooms = st.number_input(
            "Average Bedrooms",
            min_value=0.5,
            max_value=10.0,
            value=1.0,
            step=0.1,
            key=f"{prefix}_bedrooms"
        )

    with col2:
        population = st.number_input(
            "Area Population",
            min_value=1,
            max_value=50000,
            value=1000,
            key=f"{prefix}_population"
        )

        occupancy = st.number_input(
            "Average Occupancy",
            min_value=0.5,
            max_value=20.0,
            value=3.0,
            step=0.1,
            key=f"{prefix}_occupancy"
        )

        latitude = st.number_input(
            "Latitude",
            min_value=32.0,
            max_value=42.0,
            value=34.05,
            step=0.01,
            key=f"{prefix}_latitude"
        )

        longitude = st.number_input(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            value=-118.24,
            step=0.01,
            key=f"{prefix}_longitude"
        )

    return [
        income, age, rooms, bedrooms,
        population, occupancy, latitude, longitude
    ]

def save_history(name, price, values):
    st.session_state.history.append({
        "Property": name,
        "Estimated Price": price,
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "Median Income": values[0],
        "House Age": values[1]
    })

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

with st.sidebar:
    st.markdown("# 🏡 HAVEN")
    st.caption("Intelligent Property Insights")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Dashboard",
            "Price Prediction",
            "Compare Properties",
            "Analytics",
            "My History"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    if model_loaded:
        st.success("Prediction model loaded")
    else:
        st.error("Model file not found")

    st.caption("House Price Prediction System")
    st.caption("Machine Learning Project")

# ==========================================
# CHECK MODEL
# ==========================================

if not model_loaded:
    st.error(
        "Unable to load house_price_model.pkl. "
        "Please check that the model file is in the same "
        "GitHub repository folder as app.py."
    )
    st.stop()

# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("Welcome to Haven 🏡")
    st.write("Your intelligent platform for exploring property prices.")

    st.markdown("---")

    total = len(st.session_state.history)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Predictions Made", total)

    with col2:
        st.metric("Model Status", "Active")

    with col3:
        st.metric("Input Features", "8")

    st.markdown("## Explore Your Property Insights")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.subheader("🏠 Price Prediction")
            st.write(
                "Estimate a property's value using its location "
                "and housing characteristics."
            )
            if st.button("Start Prediction", use_container_width=True):
                st.session_state.quick_page = "Price Prediction"
                st.rerun()

    with right:
        with st.container(border=True):
            st.subheader("📊 Compare Properties")
            st.write(
                "Compare two properties and understand "
                "their estimated price difference."
            )
            if st.button("Compare Now", use_container_width=True):
                st.session_state.quick_page = "Compare Properties"
                st.rerun()

    st.markdown("## How It Works")

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 01")
        st.subheader("Enter Details")
        st.write("Provide the property characteristics.")

    with b:
        st.markdown("### 02")
        st.subheader("Generate Estimate")
        st.write("The trained model processes your inputs.")

    with c:
        st.markdown("### 03")
        st.subheader("View Results")
        st.write("Explore your estimated property value.")

    st.info(
        "Important: This model was trained using California housing "
        "data. Its predictions are intended for properties represented "
        "by that dataset, not Indian property valuations."
    )

# ==========================================
# PRICE PREDICTION
# ==========================================

elif page == "Price Prediction":

    st.title("Property Price Prediction")
    st.write("Enter the property details to estimate its value.")

    with st.container(border=True):
        st.subheader("Property Information")

        with st.form("prediction_form"):
            values = property_inputs("single")
            property_name = st.text_input(
                "Property Name",
                value="My Property"
            )

            submitted = st.form_submit_button(
                "✨ Predict Property Price",
                use_container_width=True
            )

        if submitted:
            try:
                price = predict_price(values)

                save_history(property_name, price, values)

                st.success("Prediction generated successfully!")

                st.markdown("### Estimated Property Value")

                st.markdown(
                    f"<h1 style='color:#765338;'>"
                    f"${price:,.2f}</h1>",
                    unsafe_allow_html=True
                )

                st.caption(
                    "This is a model estimate, not a guaranteed "
                    "market selling price."
                )

            except Exception as e:
                st.error(f"Prediction error: {e}")

# ==========================================
# COMPARE PROPERTIES
# ==========================================

elif page == "Compare Properties":

    st.title("Compare Properties")
    st.write("Enter the details of two properties to compare them.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏠 Property A")
        with st.container(border=True):
            with st.form("property_a_form"):
                values_a = property_inputs("compare_a")
                name_a = st.text_input("Property A Name", "Property A")
                submit_a = st.form_submit_button("Compare Properties")

    with col2:
        st.markdown("### 🏡 Property B")
        with st.container(border=True):
            with st.form("property_b_form"):
                values_b = property_inputs("compare_b")
                name_b = st.text_input("Property B Name", "Property B")
                submit_b = st.form_submit_button("Compare Properties")

    if submit_a or submit_b:
        st.warning(
            "Submit both property forms to compare them. "
            "Please submit the first property and then the second."
        )

    if "comparison_a" not in st.session_state:
        st.session_state.comparison_a = None

    if "comparison_b" not in st.session_state:
        st.session_state.comparison_b = None

    if submit_a:
        st.session_state.comparison_a = {
            "name": name_a,
            "values": values_a,
            "price": predict_price(values_a)
        }

    if submit_b:
        st.session_state.comparison_b = {
            "name": name_b,
            "values": values_b,
            "price": predict_price(values_b)
        }

    a = st.session_state.comparison_a
    b = st.session_state.comparison_b

    if a and b:
        st.markdown("---")
        st.subheader("Comparison Results")

        c1, c2 = st.columns(2)

        with c1:
            st.metric(a["name"], f"${a['price']:,.2f}")

        with c2:
            st.metric(b["name"], f"${b['price']:,.2f}")

        difference = abs(a["price"] - b["price"])

        st.metric("Price Difference", f"${difference:,.2f}")

        fig, ax = plt.subplots(figsize=(9, 4))
        ax.bar(
            [a["name"], b["name"]],
            [a["price"], b["price"]]
        )
        ax.set_ylabel("Estimated Price (USD)")
        ax.set_title("Property Price Comparison")
        fig.patch.set_alpha(0)
        ax.set_facecolor("#f4e9dc")
        st.pyplot(fig)
        plt.close(fig)

        if a["price"] > b["price"]:
            st.info(f"{a['name']} has the higher estimated price.")
        elif b["price"] > a["price"]:
            st.info(f"{b['name']} has the higher estimated price.")
        else:
            st.info("Both properties have the same estimated price.")

# ==========================================
# ANALYTICS
# ==========================================

elif page == "Analytics":

    st.title("Property Analytics")
    st.write("Explore the model's input features and your prediction activity.")

    st.markdown("## Model Information")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Training Records", "20,640")

    with c2:
        st.metric("Input Features", "8")

    with c3:
        st.metric("Model", "Random Forest")

    st.markdown("## Input Features")

    feature_descriptions = {
        "MedInc": "Median income in the area",
        "HouseAge": "Median house age",
        "AveRooms": "Average number of rooms",
        "AveBedrms": "Average number of bedrooms",
        "Population": "Area population",
        "AveOccup": "Average household occupancy",
        "Latitude": "Geographic latitude",
        "Longitude": "Geographic longitude"
    }

    feature_df = pd.DataFrame({
        "Feature": list(feature_descriptions.keys()),
        "Description": list(feature_descriptions.values())
    })

    st.dataframe(feature_df, use_container_width=True, hide_index=True)

    st.markdown("## Feature Importance")

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": FEATURES,
            "Importance": model.feature_importances_
        }).sort_values("Importance", ascending=True)

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.barh(
            importance_df["Feature"],
            importance_df["Importance"]
        )
        ax.set_xlabel("Importance")
        ax.set_title("Random Forest Feature Importance")
        fig.patch.set_alpha(0)
        ax.set_facecolor("#f4e9dc")
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Feature importance is not available for this model.")

    st.markdown("## Your Prediction Activity")

    if st.session_state.history:
        history_df = pd.DataFrame(st.session_state.history)
        st.line_chart(
            history_df["Estimated Price"],
            x_label="Prediction Number",
            y_label="Estimated Price (USD)"
        )
    else:
        st.info("Make some predictions to see your activity analytics.")

# ==========================================
# MY HISTORY
# ==========================================

elif page == "My History":

    st.title("My Prediction History")
    st.write("View the predictions made during your current session.")

    if st.session_state.history:

        history_df = pd.DataFrame(st.session_state.history)

        st.metric(
            "Total Predictions",
            len(history_df)
        )

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        average = history_df["Estimated Price"].mean()
        highest = history_df["Estimated Price"].max()

        c1, c2 = st.columns(2)

        with c1:
            st.metric("Average Estimated Price", f"${average:,.2f}")

        with c2:
            st.metric("Highest Estimated Price", f"${highest:,.2f}")

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

        csv = history_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download History as CSV",
            data=csv,
            file_name="house_price_history.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "No prediction history available yet. "
            "Go to Price Prediction to make your first prediction."
        )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    "<div style='text-align:center;color:#80664f;'>"
    "HAVEN | House Price Prediction System<br>"
    "Machine Learning Project"
    "</div>",
    unsafe_allow_html=True
)
