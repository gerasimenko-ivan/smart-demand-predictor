from pathlib import Path
import pandas as pd


class DataLoader:
    """Loads CSV datasets used by the Smart Demand Predictor."""

    def __init__(self, data_folder: str = "data"):
        self.data_folder = Path(data_folder)

    def load_sales_data(self) -> pd.DataFrame:
        """
        Load sales.csv into a pandas DataFrame.

        Returns:
            pd.DataFrame
        """

        file_path = self.data_folder / "sales.csv"

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        df = pd.read_csv(file_path)

        return df