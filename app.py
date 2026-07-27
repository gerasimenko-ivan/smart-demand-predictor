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
    products_df = controller.load_product_data()

    if st.button("Train model"):
        result = controller.train_forecast_model()

        st.success(
            f"Model trained! MAE = {result['mae']:.2f}"
        )

        week = result["results"]

        week = week[
            (week["Date"] >= "2026-06-20") &
            (week["Date"] <= "2026-06-26")
            ]

        st.dataframe(week)
        # st.dataframe(result["results"])

    st.success("Sales, weather data loaded successfully!")

    st.header("Sales")
    st.dataframe(sales_df)

    st.header("Weather")
    st.dataframe(weather_df)

    st.header("Holiday")
    st.dataframe(holiday_df)

    st.header("Products")
    st.dataframe(products_df)

    dataset = controller.build_training_dataset()

    st.header("Dataset")
    st.dataframe(dataset)

except Exception as e:
    st.error(str(e))