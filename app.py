import streamlit as st
import pandas as pd

from src.project_controller import ProjectController

st.set_page_config(
    page_title="Smart Demand Predictor",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Smart Demand Predictor")

# --------------------------------------------------
# Controller
# --------------------------------------------------
controller = ProjectController()

# --------------------------------------------------
# Load data
# --------------------------------------------------

try:

    sales_df = controller.load_sales_data()
    weather_df = controller.load_weather_data()
    holiday_df = controller.load_holiday_data()
    products_df = controller.load_product_data()

except Exception as e:

    st.error(f"Failed to load data:\n{e}")
    st.stop()

# --------------------------------------------------
# Train model
# --------------------------------------------------

if "model_trained" not in st.session_state:
    st.session_state["model_trained"] = False

if "forecast_result" not in st.session_state:
    st.session_state["forecast_result"] = None


train_button = st.button(
    "✨ Train AI Model",
    type="primary"
)

if train_button:

    with st.spinner("Training AI model..."):

        result = controller.train_forecast_model()

    st.session_state["forecast_result"] = result
    st.session_state["model_trained"] = True


# --------------------------------------------------
# Status
# --------------------------------------------------

if st.session_state["model_trained"]:

    st.success("🟢 AI Model: Ready")

else:

    st.warning("🔴 AI Model: Not trained. Click button  [ **✨ Train AI Model** ] above to continue.")
    st.stop()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Forecast Settings")

products = sorted(
    sales_df["Product_Name"].unique()
)

selected_product = st.sidebar.selectbox(
    "📦 Product",
    products
)

selected_date = st.sidebar.date_input(
    "📅 Week starting"
)

forecast_button = st.sidebar.button(
    "📈 Generate Forecast"
)


# --------------------------------------------------
# Forecast
# --------------------------------------------------

if forecast_button:

    result = st.session_state["forecast_result"]

    st.success(
        f"Model MAE: {result['mae']:.2f} items"
    )

    results = result["results"]

    product_results = results[
        results["Product"] == selected_product
    ]

    start_date = pd.to_datetime(selected_date)
    end_date = start_date + pd.Timedelta(days=6)

    week_results = product_results[
        (product_results["Date"] >= start_date)
        &
        (product_results["Date"] <= end_date)
    ]

    st.subheader(selected_product)

    chart = week_results.set_index("Date")

    st.line_chart(
        chart[
            [
                "Actual",
                "Predicted"
            ]
        ]
    )

    st.dataframe(week_results)