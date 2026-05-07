import streamlit as st
import requests

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Dynamic Pricing Dashboard",
    page_icon="📈",
    layout="centered"
)

# -----------------------------
# Title
# -----------------------------
st.title("📈 Dynamic Pricing & Inventory Forecasting")

st.markdown("Adjust the business parameters and predict the optimal product price.")

# -----------------------------
# User Inputs
# -----------------------------
weekly_sales = st.number_input("Weekly Sales", value=1500000)

our_price = st.slider(
    "Our Current Price",
    min_value=50.0,
    max_value=200.0,
    value=90.0
)

competitor_price = st.slider(
    "Competitor Price",
    min_value=50.0,
    max_value=200.0,
    value=100.0
)

fuel_price = st.slider(
    "Fuel Price",
    min_value=2.0,
    max_value=5.0,
    value=3.0
)

cpi = st.number_input("CPI", value=220.0)

unemployment = st.slider(
    "Unemployment Rate",
    min_value=3.0,
    max_value=12.0,
    value=7.0
)

inventory = st.number_input("Current Stock", value=25000000)

# -----------------------------
# Predict Button
# -----------------------------
if st.button("Predict Optimal Price"):

    # API URL
    url = "https://dynamicpricing-inventoryforcasting-system.onrender.com/predict"

    # JSON payload
    payload = {
    "Our_Price": our_price,
    "Competitor_Price": competitor_price,
    "Price_Gap": our_price - competitor_price,
    "Relative_Price_Index": our_price / competitor_price,
    "Elasticity": -1.2,

    "Weekly_Sales": weekly_sales,

    "sales_lag_1": 1400000,
    "sales_lag_2": 1350000,
    "sales_lag_4": 1300000,

    "sales_rolling_mean_4": 1450000,
    "sales_rolling_std_4": 80000,

    "Weeks_Until_Stockout": 20,

    "Reorder_Flag": 0
}

    try:
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            prediction = response.json()

            optimal_price = prediction["optimal_price"]

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                label="Our Price",
                value=f"₹ {our_price:.2f}"
                )

            with col2:
                st.metric(
                label="Competitor Price",
                value=f"₹ {competitor_price:.2f}"
                )

            with col3:
                st.metric(
                label="Optimal Price",
                value=f"₹ {optimal_price:.2f}",
                delta=f"{optimal_price - our_price:.2f}"
                )

            st.success("Prediction Successful ✅")

            st.metric(
                label="Optimal Price",
                value=f"₹ {prediction['optimal_price']:.2f}"
            )

        else:
            st.error(f"API Error: {response.text}")

    except Exception as e:
        st.error(f"Connection Error: {e}")