import streamlit as st

from src.project_controller import ProjectController

st.set_page_config(
    page_title="Smart Demand Predictor",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Smart Demand Predictor")

controller = ProjectController()

try:
    sales_df = controller.load_sales_data()
    weather_df = controller.load_weather_data()
    holiday_df = controller.load_holiday_data()

    st.success("Sales, weather data loaded successfully!")

    st.header("Sales")
    st.dataframe(sales_df)

    st.header("Weather")
    st.dataframe(weather_df)

    st.header("Holiday")
    st.dataframe(holiday_df)

except Exception as e:
    st.error(str(e))