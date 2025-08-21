#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
trading_simulation.py

Implements vectorized and iterative simulation functions.
Reads predictions produced by model_training.py and simulates strategies.
Saves simulation outputs to outputs/simulations/
"""
import argparse
import pandas as pd
import numpy as np
import os
from datetime import datetime

def simple_vector_backtest(pred_df, params):
    """
    Simple vectorized backtest:
    - Long if pred_proba > threshold
    - Equal weight across valid positions
    - No transaction costs in vectorized mode (easy approximation)
    """
    df = pred_df.copy()
    df = df.sort_values("date")
    df["signal"] = (df["pred_proba"] > params["prob_threshold"]).astype(int)
    # compute forward returns (assumes pred_df has return_1d precomputed)
    if "return_1d" not in df.columns:
        raise ValueError("pred_df must contain return_1d for vector backtest.")
    # aggregate per date
    grouped = df.groupby("date").apply(lambda g: (g["signal"] * g["return_1d"]).mean())
    grouped = grouped.fillna(0)
    equity = (1 + grouped).cumprod() * params["capital"]
    res = pd.DataFrame({
        "date": grouped.index,
        "daily_return": grouped.values,
        "equity": equity.values
    })
    return res

def iterative_backtest(pred_df, params):
    """
    Iterative backtest supporting position sizing, stop-loss and slippage.
    Very simple portfolio: each day we open positions in top_k tickers by pred_proba.
    """
    df = pred_df.copy()
    df = df.sort_values("date")
    capital = params["capital"]
    max_pos = params["max_positions"]
    top_k = params["top_k"]
    commission = params.get("commission_per_trade", 1.0)
    slippage = params.get("slippage_pct", 0.0)
    # Ensure return_1d present
    if "return_1d" not in df.columns:
        raise ValueError("pred_df must contain return_1d for iterative backtest.")
    equity_curve = []
    cash = capital
    holdings = {}
    dates = sorted(df["date"].unique())
    for d in dates:
        today = df[df["date"]==d].sort_values("pred_proba", ascending=False)
        picks = today.head(top_k)
        # Liquidate existing positions at EOD and realize returns
        realized = 0
        for t, info in list(holdings.items()):
            # realize return if present in today's data for ticker
            row = today[today["ticker"]==t]
            if not row.empty:
                ret = row.iloc[0]["return_1d"]
                realized += info["size"] * (1 + ret)
                # remove position
                del holdings[t]
        cash = realized if realized>0 else cash
        # Open new positions equally sized
        alloc = cash / max_pos if max_pos>0 else 0
        for _, r in picks.iterrows():
            if len(holdings) >= max_pos:
                break
            size = alloc * (1 - slippage)
            holdings[r["ticker"]] = {"size": size, "entry_date": d}
            cash -= size + commission
        total_portfolio = cash + sum([h["size"] for h in holdings.values()])
        equity_curve.append({"date": d, "equity": total_portfolio})
    return pd.DataFrame(equity_curve)

def main(args):
    os.makedirs("outputs/simulations", exist_ok=True)
    pred = pd.read_csv(args.predictions, parse_dates=["date"])
    params = {
        "capital": args.capital,
        "max_positions": args.max_positions,
        "top_k": args.top_k,
        "prob_threshold": args.prob_threshold,
        "commission_per_trade": args.commission,
        "slippage_pct": args.slippage
    }
    print("Running vectorized backtest...")
    vec = simple_vector_backtest(pred, params)
    vec.to_csv("outputs/simulations/vector_backtest.csv", index=False)
    print("Running iterative backtest...")
    itr = iterative_backtest(pred, params)
    itr.to_csv("outputs/simulations/iterative_backtest.csv", index=False)
    print("Saved simulations to outputs/simulations/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", default="models/predictions.csv")
    parser.add_argument("--capital", type=float, default=100000)
    parser.add_argument("--max_positions", type=int, default=10)
    parser.add_argument("--top_k", type=int, default=5)
    parser.add_argument("--prob_threshold", type=float, default=0.6)
    parser.add_argument("--commission", type=float, default=1.0)
    parser.add_argument("--slippage", type=float, default=0.001)
    args = parser.parse_args()
    main(args)