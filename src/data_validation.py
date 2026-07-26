import pandas as pd


class DataValidator:
    """Validates sales data before it is used by the application."""

    REQUIRED_COLUMNS = [
        "Date",
        "Product ID",
        "Product Name",
        "Sold Items Count",
        "Stock Start Count",
        "Restocked Items Count",
        "Stock End Count",
        "Promotion",
        "Unit Price (NZD)",
        "Waste Items Count"
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
            "Sold Items Count",
            "Stock Start Count",
            "Restocked Items Count",
            "Stock End Count",
            "Unit Price (NZD)",
            "Waste Items Count"
        ]

        for column in numeric_columns:

            if (df[column] < 0).any():

                raise ValueError(
                    f"Negative values found in '{column}'."
                )

    def _check_inventory_balance(self, df):

        expected_stock = (
                df["Stock Start Count"]
                + df["Restocked Items Count"]
                - df["Sold Items Count"]
                - df["Waste Items Count"]
        )

        incorrect = expected_stock != df["Stock End Count"]

        if incorrect.any():
            rows = df[incorrect].index.tolist()

            raise ValueError(
                f"Inventory balance failed for rows: {rows}"
            )