import sys
import os
import pandas as pd
import numpy as np
import pickle
from dataclasses import dataclass

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import pickle

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)


@dataclass
class DataPreprocessingConfig:
    preprocessor_obj_file_path: str = os.path.join('models', "preprocessor.pkl")


class DataPreprocessing:
    def __init__(self):
        self.config = DataPreprocessingConfig()
        
    def get_preprocessor(self, df: pd.DataFrame):
        try:
            print("Building preprocessing pipeline...")

            #separate numerical and categorical columns
            numerical_cols = df.select_dtypes(exclude = 'object').columns.tolist()
            categorical_cols = df.select_dtypes(include = "object").columns.tolist()

            # remove target columns
            if "SalePrice" in numerical_cols:
                numerical_cols.remove("SalePrice")

            # Numerical Pipeline
            num_pipeline = Pipeline(steps = [ 
                ("imputer", SimpleImputer(strategy = "median")),
                ("scaler", StandardScaler())
            ])          

            # Categorical Pipeline
            cat_pipeline = Pipeline(steps = [ 
                ("imputer", SimpleImputer(strategy = "most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown = "ignore"))
            ])

            # Combine Pipeline
            preprocessor = ColumnTransformer([
                ("num_pipeline", num_pipeline, numerical_cols),
                ("cat_pipeline", cat_pipeline, categorical_cols)
            ])

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)    

    def save_preprocessor(self, preprocessor):
        try:
            os.makedirs(os.path.dirname(self.config.preprocessor_obj_file_path), exist_ok = True)
            with open(self.config.preprocessor_obj_file_path, "wb") as f:
                pickle.dump(preprocessor, f)

            print("Preprocessor saved") 

        except Exception as e:
            raise CustomException(e, sys)



if __name__ == "__main__":
    import pandas as pd

    print("📥 Loading processed data...")

    df = pd.read_csv("data/processed/train.csv")

    print("⚙️ Initializing preprocessing...")

    dp = DataPreprocessing()

    preprocessor = dp.get_preprocessor(df)

    print("💾 Saving preprocessor...")

    dp.save_preprocessor(preprocessor)