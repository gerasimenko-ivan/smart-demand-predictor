import pandas as pd


class FeatureEngineer:

    def prepare_training_data(
        self,
        sales,
        weather,
        holidays,
        products
    ):

        df = sales.copy()

        df = df.merge(
            weather,
            on="Date",
            how="left"
        )

        df = df.merge(
            holidays,
            on="Date",
            how="left"
        )

        df = df.merge(
            products,
            on=["Product_ID", "Product_Name"],
            how="left"
        )

        df["Date"] = pd.to_datetime(df["Date"])
        df["DayOfWeek"] = df["Date"].dt.dayofweek
        df["Month"] = df["Date"].dt.month
        df["DayOfYear"] = df["Date"].dt.dayofyear
        df["Year"] = df["Date"].dt.year

        categorical_columns = [
            "Product_ID",
            "Category",
            "Storage_Type",
            "Seasonality_Group",
        ]

        df = pd.get_dummies(
            df,
            columns=categorical_columns,
            dtype = int
        )

        print(df.dtypes)

        return df