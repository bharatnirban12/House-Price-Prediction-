from fastapi import FastAPI
from app.schema import HouseData
from src.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()

pipeline = PredictionPipeline()

@app.get("/")
def home():
    return {"message":"House Price Prediction API is running"}

@app.post("/predict")
def predict(data : HouseData):
    try:
        input_data = data.dict()

        prediction = pipeline.predict(input_data)

        return {"predicted_price": prediction}

    except Exception as e:
        return {"Error": str(e)}    
