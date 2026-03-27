import os
import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dataclasses import dataclass
from sklearn.metrics import mean_squared_error, r2_score


class CustomException(Exception):
    def __init__(self, error_message, error_details: sys):
        super().__init__(error_message)

@dataclass
class ModelEvaluationConfig:
    model_path: str = os.path.join("models", "model.pkl")

class ModelEvaluation:
    def __init__(self):
        self.config = ModelEvaluationConfig()

    def evaluate(self):
        try:
            print("Loading model and test data...")

            # Load model
            with open(self.config.model_path, "rb") as f:
                model = pickle.load(f)

            # Load data
            df = pd.read_csv("data/processed/train.csv")

            X = df.drop("SalePrice", axis=1)
            y = df["SalePrice"]

            # Predictions
            y_pred = model.predict(X)

            # Metrics
            rmse = np.sqrt(mean_squared_error(y,y_pred))
            r2 = r2_score(y,y_pred)

            print(f"RMSE: {rmse}")
            print(f"R2 Score: {r2}")

            # ---------------------------
            # Residual Analysis
            # ---------------------------
            residuals = y - y_pred

            plt.figure()
            sns.histplot(residuals, bins=50)
            plt.title("Residuals, kde=True")
            plt.xlabel("Residuals")
            plt.ylabel("Frequency")
            plt.show()

            plt.figure()
            plt.scatter(y_pred, residuals)
            plt.axhline(y=0)
            plt.title("Residuals vs Predictions")
            plt.xlabel("Predictions")
            plt.ylabel("Residuals")
            plt.show()

            print("Evalution completed")

        except Exception as e:
            raise CustomException(e, sys)
    

    def get_feature_importance(self, model):
     try:
        print("\n📊 Extracting feature importance...")

        preprocessor = model.named_steps["preprocessor"]
        model_obj = model.named_steps["model"]

        feature_names = preprocessor.get_feature_names_out()

        if hasattr(model_obj, "coef_"):
            coefs = model_obj.coef_

            importance = pd.DataFrame({
                "Feature": feature_names,
                "Importance": coefs
            })

            importance = importance.sort_values(by="Importance", ascending=False)

            print("\n🔝 Top 10 Features:")
            print(importance.head(10))

        else:
            print("⚠️ Model does not support coefficients")

     except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    evaluator = ModelEvaluation()
    evaluator.evaluate()



