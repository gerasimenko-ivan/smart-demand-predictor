from src.data_loader import DataLoader
from src.data_validation import DataValidator


class ProjectController:

    def __init__(self):

        self.loader = DataLoader()
        self.validator = DataValidator()

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