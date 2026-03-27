import os
import sys

# Add the project root to the sys.path so 'src' can be imported when running this script directly
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
import numpy as np
import pickle
import mlflow
import mlflow.sklearn

from dataclasses import dataclass

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline

from src.components.data_preprocessing import DataPreprocessing


class CustomException(Exception):
    def __init__(self, error_message, error_detail : sys):
        super().__init__(error_message)


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("models", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.config = ModelTrainerConfig()  

    def evaluate_model(self, y_true, y_pred):
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        return rmse, r2

    def initiate_model_training(self):
        try:
            print("Loading Processed Data...")

            df = pd.read_csv("data/processed/train.csv")

            X = df.drop("SalePrice", axis =1)
            y = df["SalePrice"]

            # Train Test Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
            print("Preparing Preprocessing Pipeline...")

            dp = DataPreprocessing()
            preprocessor = dp.get_preprocessor(df)

            models = {
                "Linear Regression": LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "ElasticNet": ElasticNet(),
                "RandomForest": RandomForestRegressor(random_state=42),
                "XGBoost": XGBRegressor(random_state=42, verbosity=0)
            }

            params = {
                "Ridge": {
                    "model__alpha": [0.1, 1.0, 10.0]
                },
                "Lasso": {
                    "model__alpha": [0.001, 0.01, 0.1]
                },
                "ElasticNet": {
                    "model__alpha": [0.01, 0.1, 1.0],
                    "model__l1_ratio": [0.2, 0.5, 0.8]
                },

                "RandomForest": {
                    "model__n_estimators": [100, 200],
                    "model__max_depth": [None, 10, 20],
                    "model__min_samples_split": [2, 5]
                },

                "XGBoost": {
                    "model__n_estimators": [300, 500],
                    "model__learning_rate": [0.03, 0.05],
                    "model__max_depth": [4, 6, 8],
                    "model__subsample": [0.8, 1.0]
                }
            }   

            best_model = None 
            best_score = float("inf")
            best_name = ""

            print("Training Models...")

            # -------------------------------
            # MLflow Experiment
            # -------------------------------
            mlflow.set_experiment("HousePrice_Regression")

            for name, model in models.items():

                with mlflow.start_run(run_name=name):

                    print(f"\n🔹 Training {name}")

                    pipeline = Pipeline([
                        ("preprocessor", preprocessor),
                        ("model", model)
                    ])

                    if name in params:
                        grid = GridSearchCV(
                            pipeline,
                            params[name],
                            cv=5,
                            scoring= "neg_root_mean_squared_error",
                            n_jobs = -1
                        )

                        grid.fit(X_train, y_train)
                        final_model = grid.best_estimator_
                    else:
                        pipeline.fit(X_train, y_train)
                        final_model = pipeline

                    # -------------------------------
                    # Prediction
                    # -------------------------------
                    y_pred = final_model.predict(X_test)

                    rmse, r2 = self.evaluate_model(y_test, y_pred)

                    print(f"{name} RMSE:{rmse:.4f}, R2: {r2:.4f}")  

                    # -------------------------------
                    # MLflow Logging
                    # -------------------------------
                    mlflow.log_param("model_name", name)
                    mlflow.log_metric("rmse", rmse)
                    mlflow.log_metric("r2_score", r2)

                    mlflow.sklearn.log_model(final_model, "model")
                    
                    # -------------------------------
                    # Select Best Model
                    # -------------------------------
                    if rmse < best_score:
                        best_score = rmse
                        best_model = final_model
                        best_name = name
            
            print(f"\n Best Model: {best_name} with RMSE: {best_score:.4f}")
            
            # -------------------------------
            # Save best model
            # -------------------------------
            os.makedirs(os.path.dirname(self.config.trained_model_file_path), exist_ok = True)

            with open(self.config.trained_model_file_path, "wb") as f:
                pickle.dump(best_model, f)

            print("Model saved at models/model.pkl")

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.initiate_model_training()


