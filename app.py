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
if "controller" not in st.session_state:

    st.session_state["controller"] = ProjectController()

controller = st.session_state["controller"]

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
# Model status and training
# --------------------------------------------------

if not controller.is_model_trained():
    st.warning("🔴 AI Model: Not trained. Click button  [ **✨ Train AI Model** ]  to continue.")

    train_button = st.button(
        "✨ Train AI Model",
        type="primary"
    )

    if train_button:
        with st.spinner("Training AI model..."):
            controller.train_model()
        st.success("✅ Model trained successfully!")
        st.rerun()

    st.stop()

else:
    training = controller.get_training_results()

    st.success("🟢 AI Model: Ready")

    st.info(
        f"Model accuracy (MAE): {training['mae']:.2f} items"
    )

    if st.button("🔄 Retrain Model"):
        with st.spinner("Retraining..."):
            controller.train_model()
        st.rerun()

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

    start_date = pd.to_datetime(selected_date)
    end_date = start_date + pd.Timedelta(days=6)

    week = controller.predict(
        selected_product,
        start_date,
        end_date
    )

    if week.empty:
        st.warning(
            "No forecast data available for this product and period."
        )

    else:
        st.subheader(
            f"Forecast: {selected_product}"
        )

        chart = week.set_index("Date")

        st.line_chart(
            chart[
                [
                    "Actual",
                    "Predicted"
                ]
            ]
        )

        st.dataframe(
            week,
            use_container_width=True
        )

        ##### Predicted demand

        predicted_demand = round(
            week["Predicted"].sum()
        )

        st.subheader(f"📦 Predicted Demand: {predicted_demand} items")

        ##### Reorder recommendation

        current_stock = (
            sales_df[
                sales_df["Product_Name"] == selected_product
                ]
            .sort_values("Date")
            .iloc[-1]["Stock_End_Count"]
        )

        predicted_demand = round(
            week["Predicted"].sum()
        )

        reorder = controller.calculate_reorder(
            current_stock,
            predicted_demand
        )

        st.subheader(f"📦 Suggested reorder: {reorder} items (Current stock: {current_stock} items)")

        ##### Stock Risk

        risk = controller.calculate_stock_risk(
            current_stock,
            predicted_demand
        )

        if risk == "High":
            st.error("🔴 High Stock Risk")

        elif risk == "Medium":
            st.warning("🟠 Medium Stock Risk")

        else:
            st.success("🟢 Low Stock Risk")

        ##### Feature importance

        st.subheader("⭐ Feature importance")

        importance = controller.get_feature_importance()

        top_features = importance.head(7).copy()

        top_features["Importance"] = (
                top_features["Importance"] * 100
        ).round(2)

        top_features["Feature"] = (
            top_features["Feature"]
            .apply(controller.get_friendly_feature_name)
        )

        st.dataframe(
            top_features,
            hide_index=True,
            use_container_width=True
        )

        ##### AI Business Insights

        st.subheader("✨ AI Business Insights")

        insights = controller.generate_business_insights(
            selected_product,
            predicted_demand,
            current_stock,
            reorder,
            risk
        )

        for insight in insights:
            st.write(insight)


