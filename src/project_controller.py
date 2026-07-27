from src.data_loader import DataLoader
from src.data_validation import DataValidator
from src.feature_engineering import FeatureEngineer
from src.forecasting import ForecastModel


class ProjectController:

    def __init__(self):

        self.loader = DataLoader()
        self.validator = DataValidator()
        self.feature_engineer = FeatureEngineer()
        self.forecast_model = ForecastModel()

    def load_sales_data(self):

        sales_df = self.loader.load_sales_data()

        self.validator.validate_sales_data(sales_df)

        return sales_df

    def load_weather_data(self):
        weather_df = self.loader.load_weather_data()

        #TODO:
        # later:
        # self.validator.validate_weather_data(weather_df)

        return weather_df

    def load_holiday_data(self):
        holiday_df = self.loader.load_holidays_data()

        #TODO:
        # later:
        # self.validator.validate_holiday_data(holiday_df)

        return holiday_df

    def load_product_data(self):
        product_df = self.loader.load_products_data()

        #TODO:
        # later:
        # self.validator.validate_product_data(product_df)

        return product_df

    def build_training_dataset(self):
        sales_df = self.load_sales_data()

        weather_df = self.load_weather_data()

        holiday_df = self.load_holiday_data()

        product_df = self.load_product_data()

        dataset = self.feature_engineer.prepare_training_data(
            sales_df,
            weather_df,
            holiday_df,
            product_df
        )

        print(dataset.columns)

        return dataset

    def train_model(self):
        sales = self.load_sales_data()
        weather = self.load_weather_data()
        holidays = self.load_holiday_data()
        products = self.load_product_data()

        dataset = self.feature_engineer.prepare_training_data(
            sales,
            weather,
            holidays,
            products
        )

        self.forecast_model.train(dataset)
        self.forecast_model.is_trained = True

    def get_training_results(self):
        return self.forecast_model.get_results()

    def is_model_trained(self):
        return self.forecast_model.is_trained

    def predict(
            self,
            product,
            start_date,
            end_date
    ):
        return self.forecast_model.predict_product(
            product,
            start_date,
            end_date
        )