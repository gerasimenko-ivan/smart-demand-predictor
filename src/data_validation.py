import pandas as pd


class DataValidator:
    """Validates sales data before it is used by the application."""

    REQUIRED_COLUMNS = [
        "Date",
        "Product_ID",
        "Product_Name",
        "Sold_Items_Count",
        "Stock_Start_Count",
        "Restocked_Items_Count",
        "Stock_End_Count",
        "Promotion",
        "Unit_Price_NZD",
        "Waste_Items_Count"
    ]

    def validate_sales_data(self, df: pd.DataFrame):
        """
        Validate sales dataframe.

        Raises:
            ValueError if validation fails.
        """

        self._check_required_columns(df)
        self._check_missing_values(df)
        self._check_negative_values(df)
        self._check_inventory_balance(df)

        return True

    def _check_required_columns(self, df):

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    def _check_missing_values(self, df):

        if df.isnull().values.any():
            raise ValueError(
                "Dataset contains missing values."
            )

    def _check_negative_values(self, df):

        numeric_columns = [
            "Sold_Items_Count",
            "Stock_Start_Count",
            "Restocked_Items_Count",
            "Stock_End_Count",
            "Unit_Price_NZD",
            "Waste_Items_Count"
        ]

        for column in numeric_columns:

            if (df[column] < 0).any():

                raise ValueError(
                    f"Negative values found in '{column}'."
                )

    def _check_inventory_balance(self, df):

        expected_stock = (
                df["Stock_Start_Count"]
                + df["Restocked_Items_Count"]
                - df["Sold_Items_Count"]
                - df["Waste_Items_Count"]
        )

        incorrect = expected_stock != df["Stock_End_Count"]

        if incorrect.any():
            rows = df[incorrect].index.tolist()

            raise ValueError(
                f"Inventory balance failed for rows: {rows}"
            )