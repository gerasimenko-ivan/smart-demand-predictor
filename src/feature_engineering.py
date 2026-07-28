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

        # Create lag features
        df = df.sort_values(["Product_ID", "Date"])

        df["YesterdaySales"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .shift(1)
        )

        df["LastWeekSales"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .shift(7)
        )

        df["LastX2WeekSales"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .shift(14)
        )

        df["Average3Days"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .transform(
                lambda x: x.shift(1).rolling(3).mean()
            )
        )

        df["Average7Days"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .transform(
                lambda x: x.shift(1).rolling(7).mean()
            )
        )

        df["Average14Days"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .transform(
                lambda x: x.shift(1).rolling(14).mean()
            )
        )

        df["Average30Days"] = (
            df.groupby("Product_ID")["Sold_Items_Count"]
            .transform(
                lambda x: x.shift(1).rolling(30).mean()
            )
        )

        # Restore chronological order
        df = df.sort_values("Date").reset_index(drop=True)

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
        df["DaysUntilExpiry"] = df["Shelf_Life_Days"]

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