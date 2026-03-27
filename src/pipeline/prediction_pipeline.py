import os
import pickle
import pandas as pd
import numpy as np


class PredictionPipeline:
    def __init__(self):
        self.model_path = "models/model.pkl"
        self.train_data_path = "data/processed/train.csv"
        self.model = self.load_model()
        self.template = self.get_template()

    def load_model(self):
        with open(self.model_path, "rb") as f:
            model = pickle.load(f)
        return model

    def get_template(self):
        df = pd.read_csv(self.train_data_path)
        template = df.drop("SalePrice", axis=1).iloc[0].to_dict()
        return template

    def predict(self, data: dict):
        try:
            # 🔥 Fill missing features using preloaded template
            template_copy = self.template.copy()
            template_copy.update(data)

            df = pd.DataFrame([template_copy])

            pred = self.model.predict(df)[0]

            # Convert back to actual price
            return float(np.expm1(pred))

        except Exception as e:
            print("❌ Prediction error:", e)
            raise e