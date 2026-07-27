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

        df["IsWeekend"] = (df["DayOfWeek"] >= 5).astype(int)

        df["PromotionFlag"] = (df["Promotion"] == "Yes").astype(int)

        df["HolidayFlag"] = (
            df["Holiday"].fillna("No") != "No"
        ).astype(int)

        df["RainFlag"] = (
            df["Precipitation"] > 0
        ).astype(int)

        return df