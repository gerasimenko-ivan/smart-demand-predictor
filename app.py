import streamlit as st

from src.data_loader import DataLoader
from src.data_validation import DataValidator


st.set_page_config(
    page_title="Smart Demand Predictor",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Smart Demand Predictor")

loader = DataLoader()
validator = DataValidator()

try:
    sales_df = loader.load_sales_data()

    validator.validate_sales_data(sales_df)

    st.success("Sales data loaded successfully!")

    st.write(f"Rows: {len(sales_df)}")
    st.write(f"Columns: {len(sales_df.columns)}")

    st.dataframe(sales_df)

except Exception as e:
    st.error(str(e))