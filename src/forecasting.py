from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

import pandas as pd


class ForecastModel:

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def prepare_data(self, df):

        # Target
        y = df["Sold_Items_Count"]

        # Remove columns that should not be used directly
        X = df.drop(
            columns=[
                "Sold_Items_Count",
                "Date",
                "Product_Name"
            ],
            errors="ignore"
        )

        # Convert text columns to numbers
        X = pd.get_dummies(X)

        return X, y


    def train(self, df):

        X, y = self.prepare_data(df)

        # Important:
        # do NOT shuffle time series data
        split_index = int(len(X) * 0.8)

        X_train = X.iloc[:split_index]
        X_test = X.iloc[split_index:]

        y_train = y.iloc[:split_index]
        y_test = y.iloc[split_index:]


        self.model.fit(
            X_train,
            y_train
        )


        predictions = self.model.predict(
            X_test
        )


        mae = mean_absolute_error(
            y_test,
            predictions
        )

        return mae


    def predict(self, df):

        X, _ = self.prepare_data(df)

        predictions = self.model.predict(X)

        return predictions