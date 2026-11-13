
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from pathlib import Path
from datetime import datetime

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="Haven | Property Insights",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# DESIGN
# =====================================

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(255,255,255,.8), transparent 35%),
        linear-gradient(135deg, #f4e9dc, #dfc7ad, #efe1d0);
    color: #493629;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4 {
    color: #493629 !important;
}

section[data-testid="stSidebar"] {
    background: rgba(255,248,239,.85);
    border-right: 1px solid white;
}

section[data-testid="stSidebar"] * {
    color: #513d2e;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,.55);
    border: 1px solid rgba(255,255,255,.8);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 6px 20px rgba(80,50,25,.08);
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,250,244,.55);
    border: 1px solid rgba(255,255,255,.8);
    border-radius: 20px;
    padding: 12px;
    box-shadow: 0 8px 25px rgba(91,61,36,.08);
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #9c7654, #694a32);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: .65rem 1.2rem;
    font-weight: 600;
    transition: .3s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #765338, #4e3524);
    transform: translateY(-2px);
}

.stTextInput input,
.stNumberInput input,
.stTextArea textarea {
    background: rgba(255,255,255,.75) !important;
    color: #493629 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] {
    background: rgba(255,255,255,.75);
    border-radius: 10px;
}

hr {
    border-color: rgba(105,74,50,.18);
}
</style>
""", unsafe_allow_html=True)

# =====================================
# LOAD MODEL
# =====================================

@st.cache_resource
def load_model():
    model_file = Path(__file__).parent / "house_price_model.pkl"
    return joblib.load(model_file)

try:
    model = load_model()
except Exception as error:
    st.error("Unable to load the house price model.")
    st.code(str(error))
    st.info(
        "Check that house_price_model.pkl is uploaded "
        "in the same GitHub folder as app.py."
    )
    st.stop()

# =====================================
# SESSION DATA
# =====================================

if "history" not in st.session_state:
    st.session_state.history = []

if "comparison_a" not in st.session_state:
    st.session_state.comparison_a = None

if "comparison_b" not in st.session_state:
    st.session_state.comparison_b = None

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

# =====================================
# FUNCTIONS
# =====================================

def predict_price(values):
    input_data = pd.DataFrame([values], columns=FEATURES)
    prediction = float(model.predict(input_data)[0])
    return max(0, prediction * 100000)


def property_inputs(prefix):
    c1, c2 = st.columns(2)

    with c1:
        income = st.number_input(
            "Median Income (in $10,000s)",
            min_value=0.5,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key=prefix + "_income"
        )

        age = st.number_input(
            "House Age",
            min_value=1,
            max_value=100,
            value=25,
            key=prefix + "_age"
        )

        rooms = st.number_input(
            "Average Rooms",
            min_value=1.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
            key=prefix + "_rooms"
        )

        bedrooms = st.number_input(
            "Average Bedrooms",
            min_value=0.5,
            max_value=10.0,
            value=1.0,
            step=0.1,
            key=prefix + "_bedrooms"
        )

    with c2:
        population = st.number_input(
            "Area Population",
            min_value=1,
            max_value=50000,
            value=1000,
            key=prefix + "_population"
        )

        occupancy = st.number_input(
            "Average Occupancy",
            min_value=0.5,
            max_value=20.0,
            value=3.0,
            step=0.1,
            key=prefix + "_occupancy"
        )

        latitude = st.number_input(
            "Latitude",
            min_value=32.0,
            max_value=42.0,
            value=34.05,
            step=0.01,
            key=prefix + "_latitude"
        )

        longitude = st.number_input(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            value=-118.24,
            step=0.01,
            key=prefix + "_longitude"
        )

    return [
        income, age, rooms, bedrooms,
        population, occupancy, latitude, longitude
    ]


def add_history(name, price):
    st.session_state.history.append({
        "Property": name,
        "Estimated Price": price,
        "Date": datetime.now().strftime("%d-%m-%Y %H:%M")
    })


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:
    st.markdown("# 🏡 HAVEN")
    st.caption("Your Property Insights")
    st.divider()

    page = st.radio(
        "MENU",
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
    st.success("App is ready")
    st.caption("House Price Prediction")

# =====================================
# DASHBOARD
# =====================================

if page == "Dashboard":

    st.title("Welcome to Haven 🏡")
    st.write("Discover property insights through intelligent price estimates.")

    st.markdown("---")

    total = len(st.session_state.history)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Predictions", total)
    c2.metric("App Status", "Active")
    c3.metric("Available Features", "5")

    st.markdown("## Explore Your Dashboard")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.subheader("🏠 Price Prediction")
            st.write("Estimate the value of a property.")
            st.button(
                "Go to Prediction",
                key="dashboard_prediction",
                use_container_width=True,
                on_click=lambda: st.session_state.update(
                    selected_page="Price Prediction"
                )
            )

    with right:
        with st.container(border=True):
            st.subheader("📊 Compare Properties")
            st.write("Compare estimated prices of two properties.")
            st.button(
                "Compare Properties",
                key="dashboard_compare",
                use_container_width=True,
                on_click=lambda: st.session_state.update(
                    selected_page="Compare Properties"
                )
            )

    if "selected_page" in st.session_state:
        if st.session_state.selected_page in [
            "Price Prediction", "Compare Properties"
        ]:
            st.info(
                "Choose the page from the navigation menu "
                "on the left to continue."
            )

    st.markdown("## Simple Steps")

    a, b, c = st.columns(3)

    a.markdown("### 01")
    a.write("Enter property details")

    b.markdown("### 02")
    b.write("Generate price estimate")

    c.markdown("### 03")
    c.write("View your results")

    st.info(
        "This model was trained using California housing data. "
        "It is not suitable for estimating Indian property market prices."
    )

# =====================================
# PRICE PREDICTION
# =====================================

elif page == "Price Prediction":

    st.title("Property Price Prediction")
    st.write("Enter the property information below.")

    with st.container(border=True):

        with st.form("prediction_form"):

            st.subheader("Property Details")

            values = property_inputs("single")

            property_name = st.text_input(
                "Property Name",
                value="My Property"
            )

            submit = st.form_submit_button(
                "✨ Predict Price",
                use_container_width=True
            )

        if submit:
            try:
                price = predict_price(values)
                add_history(property_name, price)

                st.success("Your prediction is ready!")

                st.markdown("### Estimated Property Value")

                st.markdown(
                    f"<h1 style='color:#765338;'>${price:,.2f}</h1>",
                    unsafe_allow_html=True
                )

                st.caption(
                    "This is an estimated value, not a guaranteed selling price."
                )

            except Exception as error:
                st.error("Unable to generate prediction.")
                st.code(str(error))

# =====================================
# COMPARE PROPERTIES
# =====================================

elif page == "Compare Properties":

    st.title("Compare Properties")
    st.write("Enter two properties to compare their estimated prices.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏠 Property A")

        with st.container(border=True):
            with st.form("compare_form_a"):
                name_a = st.text_input("Property A Name", "Property A")
                values_a = property_inputs("compare_a")
                submit_a = st.form_submit_button("Save Property A")

    with col2:
        st.subheader("🏡 Property B")

        with st.container(border=True):
            with st.form("compare_form_b"):
                name_b = st.text_input("Property B Name", "Property B")
                values_b = property_inputs("compare_b")
                submit_b = st.form_submit_button("Save Property B")

    if submit_a:
        st.session_state.comparison_a = {
            "name": name_a,
            "price": predict_price(values_a)
        }
        st.success("Property A saved.")

    if submit_b:
        st.session_state.comparison_b = {
            "name": name_b,
            "price": predict_price(values_b)
        }
        st.success("Property B saved.")

    a = st.session_state.comparison_a
    b = st.session_state.comparison_b

    if a and b:

        st.markdown("---")
        st.subheader("Comparison Results")

        x, y = st.columns(2)

        x.metric(a["name"], f"${a['price']:,.2f}")
        y.metric(b["name"], f"${b['price']:,.2f}")

        difference = abs(a["price"] - b["price"])

        st.metric("Price Difference", f"${difference:,.2f}")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.bar(
            [a["name"], b["name"]],
            [a["price"], b["price"]]
        )

        ax.set_ylabel("Estimated Price (USD)")
        ax.set_title("Property Comparison")

        st.pyplot(fig)
        plt.close(fig)

        if a["price"] > b["price"]:
            st.info(a["name"] + " has the higher estimated price.")
        elif b["price"] > a["price"]:
            st.info(b["name"] + " has the higher estimated price.")
        else:
            st.info("Both properties have equal estimated prices.")

    else:
        st.info("Save both properties to see the comparison.")

# =====================================
# ANALYTICS
# =====================================

elif page == "Analytics":

    st.title("Property Analytics")
    st.write("Your property prediction insights at a glance.")

    history = st.session_state.history

    if history:

        df = pd.DataFrame(history)

        total = len(df)
        average = df["Estimated Price"].mean()
        highest = df["Estimated Price"].max()
        lowest = df["Estimated Price"].min()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Predictions", total)
        c2.metric("Average Price", f"${average:,.0f}")
        c3.metric("Highest Price", f"${highest:,.0f}")
        c4.metric("Lowest Price", f"${lowest:,.0f}")

        st.markdown("---")

        st.subheader("Property Price Trends")

        st.line_chart(
            df["Estimated Price"].reset_index(drop=True),
            x_label="Prediction Number",
            y_label="Estimated Price (USD)"
        )

        st.markdown("---")

        st.subheader("Property Price Comparison")

        chart_data = df.set_index("Property")[["Estimated Price"]]
        st.bar_chart(chart_data)

        st.markdown("---")

        st.subheader("Recent Prediction Activity")

        display_df = df.copy()
        display_df["Estimated Price"] = display_df[
            "Estimated Price"
        ].map(lambda value: f"${value:,.2f}")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info(
            "No analytics available yet. Make your first prediction "
            "to see your property analytics here."
        )

# =====================================
# MY HISTORY
# =====================================

elif page == "My History":

    st.title("My Prediction History")
    st.write("View and download your recent property predictions.")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.metric("Total Predictions", len(df))

        display_df = df.copy()
        display_df["Estimated Price"] = display_df[
            "Estimated Price"
        ].map(lambda value: f"${value:,.2f}")

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Average Price",
            f"${df['Estimated Price'].mean():,.2f}"
        )

        c2.metric(
            "Highest Price",
            f"${df['Estimated Price'].max():,.2f}"
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download History as CSV",
            data=csv,
            file_name="property_history.csv",
            mime="text/csv"
        )

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info(
            "Your history is empty. Make a prediction to get started."
        )

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.markdown(
    "<div style='text-align:center;color:#80664f;'>"
    "HAVEN | Property Insights<br>"
    "House Price Prediction System"
    "</div>",
    unsafe_allow_html=True
)
