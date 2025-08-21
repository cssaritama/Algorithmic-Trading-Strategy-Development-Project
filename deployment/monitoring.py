#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 



"""
monitoring.py — simple monitoring & alerting stubs.

Example: detect large drawdown or sudden model score drop and send a Telegram message.
Users must set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID as environment variables if they want alerts.
"""
import os
import requests

def send_telegram(msg):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram credentials not set; skipping alert.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": msg})

def check_drawdown_and_alert(equity_csv):
    import pandas as pd
    df = pd.read_csv(equity_csv, parse_dates=["date"])
    df = df.sort_values("date")
    roll_max = df["equity"].cummax()
    drawdown = df["equity"] / roll_max - 1.0
    mdd = drawdown.min()
    if mdd < -0.2:
        send_telegram(f"Alert: Max drawdown reached {mdd:.2%}")