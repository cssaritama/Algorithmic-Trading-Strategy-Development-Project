#**Author:** Carlos Stalin Saritama Atopo  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
data_collection.py

Collects market data from multiple sources (yfinance, AlphaVantage, Quandl, FRED, NewsAPI).
If --use-sample is passed, it will create synthetic data so reviewers can run without API keys.

Outputs: data/raw.parquet
"""
import argparse
import os
import pandas as pd
import yfinance as yf
from scripts.utils import make_sample_price_series, save_df_parquet

def download_yfinance(tickers, start, end, interval="1d"):
    frames = []
    for t in tickers:
        print(f"Downloading {t} from yfinance...")
        df = yf.download(t, start=start, end=end, interval=interval, progress=False)
        if df.empty:
            print(f"Warning: {t} returned empty data.")
            continue
        df = df.reset_index()
        df["ticker"] = t
        frames.append(df[["Date","ticker","Open","High","Low","Close","Volume"]].rename(columns={
            "Date":"date","Open":"open","High":"high","Low":"low","Close":"close","Volume":"volume"
        }))
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()

def main(args):
    os.makedirs("data", exist_ok=True)
    if args.use_sample:
        print("Generating sample synthetic data...")
        df_list = []
        for t in args.tickers:
            df = make_sample_price_series(ticker=t, start=args.start, periods=600)
            df_list.append(df)
        all_df = pd.concat(df_list, ignore_index=True)
        save_df_parquet(all_df, "data/raw.parquet")
        print("Saved synthetic sample to data/raw.parquet")
        return

    # Try downloading real data (requires internet & yfinance)
    df = download_yfinance(args.tickers, args.start, args.end, args.interval)
    if df.empty:
        raise RuntimeError("No data downloaded. Try --use-sample mode.")
    save_df_parquet(df, "data/raw.parquet")
    print("Saved raw data to data/raw.parquet")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tickers", nargs="+", default=["AAPL","MSFT","SPY"])
    parser.add_argument("--start", default="2018-01-01")
    parser.add_argument("--end", default="2024-12-31")
    parser.add_argument("--interval", default="1d")
    parser.add_argument("--use-sample", action="store_true")
    args = parser.parse_args()
    main(args)