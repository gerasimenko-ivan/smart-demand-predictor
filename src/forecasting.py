from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import pandas as pd


class ForecastModel:

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        self.results = None
        self.feature_importance = None
        self.is_trained = False

    def prepare_data(self, df):

        # Target
        y = df["Sold_Items_Count"]

        # Remove columns that should not be used directly
        X = df.drop(
            columns=[
                "Sold_Items_Count",
                "Date",
                "Product_Name",
                "Promotion_Eligible",
            ],
            errors="ignore"
        )

        # Convert text columns to numbers
        X = pd.get_dummies(X)

        self.validate_features(X)

        return {
            "X": X,
            "y": y,
            "dates": df["Date"],
            "products": df["Product_Name"]
        }

    def validate_features(self, X):

        non_numeric = X.select_dtypes(
            exclude=["number"]
        )

        if not non_numeric.empty:
            raise ValueError(
                f"Non-numeric columns: {list(non_numeric.columns)}"
            )

        # TODO: check for missing values
        # missing = X.isnull().sum()
        #
        # missing = missing[missing > 0]
        #
        # if not missing.empty:
        #     raise ValueError(
        #         f"Missing values:\n{missing}"
        #     )


    def train(self, df):
        # X, y, dates, product_names = self.prepare_data(df)
        data = self.prepare_data(df)

        X = data["X"]
        y = data["y"]
        dates = data["dates"]
        products = data["products"]

        X_train, X_test, y_train, y_test, dates_train, dates_test, products_train, products_test = self.split_data(X, y, dates, products)

        print(f"Training rows: {len(X_train)}")
        print(f"Testing rows: {len(X_test)}")

        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)

        mae = mean_absolute_error(y_test, predictions)

        results = pd.DataFrame({
            "Date": dates_test.values,
            "Product": products_test.values,
            "Actual": y_test.values,
            "Predicted": predictions
        })

        results["Error"] = (
                results["Predicted"] - results["Actual"]
        )

        self.results = {
            "mae": mae,
            "results": results
        }

        self.is_trained = True

        importance = pd.DataFrame({

            "Feature": X.columns,

            "Importance": self.model.feature_importances_

        })

        importance = importance.sort_values(
            "Importance",
            ascending=False
        )

        self.feature_importance = importance

        return self.results

    def get_results(self):
        return self.results

    def predict_product(
            self,
            product_name,
            start_date,
            end_date
    ):

        if not self.is_trained:
            raise RuntimeError(
                "Model has not been trained."
            )

        df = self.results["results"]

        product = df[
            df["Product"] == product_name
            ]

        product = product[
            (product["Date"] >= start_date)
            &
            (product["Date"] <= end_date)
            ]

        return product

    def predict(self, df):
        X, _, _, _ = self.prepare_data(df)

        predictions = self.model.predict(X)

        return predictions

    def split_data(self, X, y, dates, products):
        # Important:
        # do NOT shuffle time series data
        split_index = int(len(X) * 0.8)

        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]

        dates_train = dates.iloc[:split_index]
        dates_test = dates.iloc[split_index:]

        products_train = products.iloc[:split_index]
        products_test = products.iloc[split_index:]

        return X_train, X_test, y_train, y_test, dates_train, dates_test, products_train, products_test