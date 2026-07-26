from pathlib import Path
import pandas as pd


class DataLoader:
    """Loads CSV datasets used by the Smart Demand Predictor."""

    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)

    def load_csv(self, filename: str) -> pd.DataFrame:
        """
        Generic CSV loader.

        Args:
            filename: CSV file name inside data folder.

        Returns:
            pandas DataFrame
        """

        file_path = self.data_folder / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        df = pd.read_csv(file_path)

        print(
            f"Loaded {filename}: {len(df)} rows"
        )

        return df

    def load_sales_data(self) -> pd.DataFrame:
        """ Load historical sales data """
        df = self.load_csv("sales.csv")

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def load_weather_data(self) -> pd.DataFrame:
        df = self.load_csv("weather.csv")

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    def load_holidays_data(self) -> pd.DataFrame:
        df = self.load_csv("holidays.csv")

        df["Date"] = pd.to_datetime(df["Date"])

        return df

    # def load_products_data(self) -> pd.DataFrame:
    #     return self.load_csv("products.csv")