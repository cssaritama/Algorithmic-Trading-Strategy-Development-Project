#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 


from fastapi import FastAPI
import pandas as pd
import os
from typing import List
from pydantic import BaseModel

app = FastAPI(title="AlphaTrader-ML API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/latest_trades")
def latest_trades(limit: int = 10):
    path = "outputs/simulations/iterative_backtest.csv"
    if not os.path.exists(path):
        return {"error": "No simulations found. Run pipeline first."}
    df = pd.read_csv(path)
    return df.tail(limit).to_dict(orient="records")

class PredictRequest(BaseModel):
    tickers: List[str]

@app.post("/predict")
def predict(req: PredictRequest):
    pred_path = "models/predictions.csv"
    if os.path.exists(pred_path):
        df = pd.read_csv(pred_path)
        df = df[df["ticker"].isin(req.tickers)]
        return df.sort_values("pred_proba", ascending=False).head(20).to_dict(orient="records")
    return {"message": "No predictions available. Run the pipeline first or use --use-sample."}