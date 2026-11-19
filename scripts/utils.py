#**Author:** Carlos Stalin Saritama Atopo  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 


"""
utils.py — helper utilities used across scripts
"""
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def save_df_parquet(df, path):
    ensure_dir(os.path.dirname(path))
    df.to_parquet(path)

def load_df_parquet(path):
    return pd.read_parquet(path)

def make_sample_price_series(ticker="SAMPLE", start="2020-01-01", periods=500, seed=0):
    """Generate a synthetic price series for testing without API keys."""
    np.random.seed(seed)
    dates = pd.bdate_range(start=start, periods=periods)
    returns = np.random.normal(loc=0.0005, scale=0.02, size=periods)
    price = 100 * np.exp(np.cumsum(returns))
    df = pd.DataFrame({
        "date": dates,
        "ticker": ticker,
        "open": price * (1 - np.random.uniform(0,0.002,size=periods)),
        "high": price * (1 + np.random.uniform(0,0.005,size=periods)),
        "low": price * (1 - np.random.uniform(0,0.005,size=periods)),
        "close": price,
        "volume": np.random.randint(100000, 1000000, size=periods)
    })
    df = df.set_index("date").reset_index()
    return df

def save_model(obj, path):
    ensure_dir(os.path.dirname(path))
    joblib.dump(obj, path)

def load_model(path):
    return joblib.load(path)