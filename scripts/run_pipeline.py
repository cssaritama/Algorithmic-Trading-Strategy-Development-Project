#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
run_pipeline.py

End-to-end runner script. Executes:
1. data_collection.py
2. feature_engineering.py
3. model_training.py
4. trading_simulation.py
5. performance_analysis.py

Supports --use-sample (recommended for reviewers).
"""
import argparse
import subprocess
import sys

def run(cmd):
    print("RUN:", cmd)
    res = subprocess.run([sys.executable] + cmd.split(), check=True)
    return res

def main(args):
    if args.use_sample:
        run(f"scripts/data_collection.py --use-sample --tickers {' '.join(args.tickers)} --start {args.start}")
    else:
        run(f"scripts/data_collection.py --tickers {' '.join(args.tickers)} --start {args.start} --end {args.end}")
    run("scripts/feature_engineering.py --input data/raw.parquet --output data/processed.parquet")
    run("scripts/model_training.py --input data/processed.parquet --target up_1d")
    run("scripts/trading_simulation.py --predictions models/predictions.csv --capital 100000")
    run("scripts/performance_analysis.py --sim outputs/simulations/iterative_backtest.csv")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--use-sample", action="store_true")
    parser.add_argument("--tickers", nargs="+", default=["AAPL","MSFT","SPY"])
    parser.add_argument("--start", default="2018-01-01")
    parser.add_argument("--end", default="2024-12-31")
    args = parser.parse_args()
    main(args)