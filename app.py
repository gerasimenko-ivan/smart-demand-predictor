import streamlit as st
import pandas as pd

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

    st.sidebar.header("Forecast Settings")

    products = sorted(
        sales_df["Product_Name"].unique()
    )

    selected_product = st.sidebar.selectbox(
        "📦 Product",
        sorted(products)
    )

    selected_date = st.sidebar.date_input(
        "📅 Week starting"
    )

    # end_date = st.sidebar.date_input(
    #     "End date"
    # )

    forecast_button = st.sidebar.button(
        "📈 Generate Forecast"
    )

    if forecast_button:
        result = controller.train_forecast_model()

        st.success(
            f"Model trained (MAE = {result['mae']:.2f})"
        )

        results = result["results"]

        product_results = results[
            results["Product"] == selected_product
            ]

        start_date = pd.to_datetime(selected_date)

        end_date = start_date + pd.Timedelta(days=6)

        week_results = product_results[
            (product_results["Date"] >= start_date) &
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

    # if st.button("Train model"):
    #     result = controller.train_forecast_model()
    #
    #     st.success(
    #         f"Model trained! MAE = {result['mae']:.2f}"
    #     )
    #
    #     week = result["results"]
    #
    #     week = week[
    #         (week["Date"] >= "2026-06-20") &
    #         (week["Date"] <= "2026-06-26")
    #         ]
    #
    #     st.dataframe(week)
    #
    #     # chart_df = week.set_index("Date")
    #     #
    #     # st.line_chart(
    #     #     chart_df[["Actual", "Predicted"]]
    #     # )
    #
    #     # st.dataframe(result["results"])

    # st.success("Sales, weather data loaded successfully!")
    #
    # st.header("Sales")
    # st.dataframe(sales_df)
    #
    # st.header("Weather")
    # st.dataframe(weather_df)
    #
    # st.header("Holiday")
    # st.dataframe(holiday_df)
    #
    # st.header("Products")
    # st.dataframe(products_df)
    #
    # dataset = controller.build_training_dataset()
    #
    # st.header("Dataset")
    # st.dataframe(dataset)

except Exception as e:
    st.error(str(e))