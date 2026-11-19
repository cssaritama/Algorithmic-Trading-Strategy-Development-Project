#**Author:** Carlos Stalin Saritama Atopo  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 

"""
model_training.py

Train multiple models (RandomForest, XGBoost, LSTM) and save predictions.
Uses simple train/test split. Supports --use-sample for demo mode.
"""
import argparse
import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

from scripts.utils import save_model, load_df_parquet

def prepare_dataset(df, target="up_1d"):
    # Drop rows with NaNs in target/features
    features = [
        c for c in df.columns if c not in ["date","ticker","open","high","low","close","volume","return_1d","return_5d"]
    ]
    df = df.dropna(subset=[target])
    X = df[features].fillna(0)
    y = df[target]
    return X, y, df

def train_random_forest(X_train, y_train):
    clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    return clf

def main(args):
    os.makedirs("models", exist_ok=True)
    df = load_df_parquet(args.input)
    X, y, orig = prepare_dataset(df, target=args.target)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print("Training RandomForest...")
    rf = train_random_forest(X_train, y_train)
    save_model(rf, "models/random_forest.joblib")
    preds = rf.predict_proba(X_test)[:,1]
    print(classification_report(y_test, (preds>0.5).astype(int)))
    # Save a CSV with predictions aligned to original rows
    test_idx = X_test.index
    out = orig.loc[test_idx, ["date","ticker","close"]].copy()
    out["pred_proba"] = preds
    out.to_csv("models/predictions.csv", index=False)
    print("Saved model and predictions to models/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed.parquet")
    parser.add_argument("--target", default="up_1d")
    args = parser.parse_args()
    main(args)