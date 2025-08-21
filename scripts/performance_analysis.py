#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
performance_analysis.py

Compute financial performance metrics: CAGR, Sharpe, Max Drawdown, rolling returns.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def cagr(equity_series, periods_per_year=252):
    returns = equity_series.pct_change().dropna()
    n = len(returns)
    total_return = equity_series.iloc[-1] / equity_series.iloc[0]
    years = n / periods_per_year
    return total_return ** (1/years) - 1

def sharpe(returns, risk_free=0.0, periods_per_year=252):
    ann_ret = returns.mean() * periods_per_year
    ann_vol = returns.std() * (periods_per_year ** 0.5)
    return (ann_ret - risk_free) / ann_vol if ann_vol != 0 else np.nan

def max_drawdown(equity):
    roll_max = equity.cummax()
    drawdown = equity / roll_max - 1.0
    return drawdown.min()

def analyze(sim_csv, output_dir="outputs/analysis"):
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(sim_csv, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["daily_return"] = df["equity"].pct_change().fillna(0)
    c = cagr(df["equity"])
    s = sharpe(df["daily_return"])
    mdd = max_drawdown(df["equity"])
    summary = {
        "CAGR": c,
        "Sharpe": s,
        "Max Drawdown": mdd
    }
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(os.path.join(output_dir, "summary.csv"), index=False)
    # Plot equity
    plt.figure(figsize=(10,6))
    plt.plot(df["date"], df["equity"])
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Equity")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "equity_curve.png"))
    print("Saved analysis results to", output_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", default="outputs/simulations/iterative_backtest.csv")
    args = parser.parse_args()
    analyze(args.sim)