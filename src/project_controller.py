from src.data_loader import DataLoader
from src.data_validation import DataValidator
from src.feature_engineering import FeatureEngineer


class ProjectController:

    def __init__(self):

        self.loader = DataLoader()
        self.validator = DataValidator()
        self.feature_engineer = FeatureEngineer()

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

        dataset = self.feature_engineer.build_feature_dataset(
            sales_df,
            weather_df,
            holiday_df,
            product_df
        )

        return dataset