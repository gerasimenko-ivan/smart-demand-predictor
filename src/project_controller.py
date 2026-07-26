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