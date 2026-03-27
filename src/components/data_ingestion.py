import os
import sys
import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

# Custom exception (we will define later in utils)
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("data", "raw", "train.csv")
    test_data_path: str = os.path.join("data", "raw", "test.csv")
    raw_data_path: str = os.path.join("data", "raw", "full_data.csv")


class DataIngestion:
    def __init__(self):
        self.config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        try:
            print("📥 Starting Data Ingestion...")

            # Load dataset
            df = pd.read_csv("notebooks/data/train.csv")  # adjust path if needed

            # Create directories if not exist
            os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)

            # Save raw copy
            df.to_csv(self.config.raw_data_path, index=False)

            print("📁 Raw data saved")

            # Train-Test Split
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.config.train_data_path, index=False)
            test_set.to_csv(self.config.test_data_path, index=False)

            print("✅ Data Ingestion Completed")

            return (
                self.config.train_data_path,
                self.config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)