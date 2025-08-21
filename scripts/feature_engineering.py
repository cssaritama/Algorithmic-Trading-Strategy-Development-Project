#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
feature_engineering.py

Reads raw.parquet and generates engineered features (technical indicators, volatility, momentum, dummies).
Saves processed dataset to data/processed.parquet
"""
import argparse
import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands
from ta.trend import SMAIndicator, EMAIndicator
from scripts.utils import load_df_parquet, save_df_parquet

def compute_features(df):
    df = df.sort_values(["ticker","date"]).copy()
    feats = []
    out_frames = []
    for t, g in df.groupby("ticker"):
        g = g.reset_index(drop=True)
        g["close"] = g["close"].astype(float)
        g["return_1d"] = g["close"].pct_change().shift(-1)  # forward return candidate
        g["return_5d"] = g["close"].pct_change(5).shift(-5)
        # Moving averages
        for w in [5,10,20,50,200]:
            g[f"ma_{w}"] = g["close"].rolling(w).mean()
        # EMA
        g["ema_12"] = EMAIndicator(g["close"], window=12).ema_indicator()
        g["ema_26"] = EMAIndicator(g["close"], window=26).ema_indicator()
        # MACD
        g["macd"] = g["ema_12"] - g["ema_26"]
        g["macd_signal"] = g["macd"].ewm(span=9).mean()
        # RSI
        g["rsi_14"] = RSIIndicator(g["close"], window=14).rsi()
        # ATR
        g["atr_14"] = AverageTrueRange(high=g["high"], low=g["low"], close=g["close"], window=14).average_true_range()
        # Bollinger
        boll = BollingerBands(close=g["close"], window=20, window_dev=2)
        g["boll_mid"] = boll.bollinger_mavg()
        g["boll_upper"] = boll.bollinger_hband()
        g["boll_lower"] = boll.bollinger_lband()
        # Volatility and momentum
        g["volatility_21"] = g["close"].pct_change().rolling(21).std()
        g["momentum_10"] = g["close"].pct_change(10)
        g["overnight_return"] = (g["open"] - g["close"].shift(1)) / g["close"].shift(1)
        # VWAP approximation
        g["vwap"] = (g["close"] * g["volume"]).cumsum() / g["volume"].cumsum()
        # Volume change
        g["volume_change_5d"] = g["volume"].pct_change(5)
        # 52-week high/low flags
        g["52w_high"] = g["close"] >= g["close"].rolling(252).max() * 0.98
        g["52w_low"] = g["close"] <= g["close"].rolling(252).min() * 1.02
        # Higher moments
        g["skewness_21"] = g["close"].pct_change().rolling(21).skew()
        g["kurtosis_21"] = g["close"].pct_change().rolling(21).kurt()
        # Beta vs benchmark if benchmark provided (placeholder)
        g["beta_21"] = np.nan
        out_frames.append(g)
    res = pd.concat(out_frames, ignore_index=True)
    # Define a simple classification target
    res["up_1d"] = (res["return_1d"] > 0).astype(int)
    return res

def main(args):
    df = load_df_parquet(args.input)
    processed = compute_features(df)
    save_df_parquet(processed, args.output)
    print(f"Saved processed data to {args.output}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw.parquet")
    parser.add_argument("--output", default="data/processed.parquet")
    args = parser.parse_args()
    main(args)