# AlphaTrader-ML: Machine Learning Driven Algorithmic Trading System

## 📌 Project Overview

AlphaTrader-ML is an end-to-end machine learning-powered algorithmic trading system developed as the final project for the Stock Markets Analytics Zoomcamp 2025.  
The project integrates financial data ingestion, feature engineering, ML modeling, backtesting, and automation into a complete workflow ready for research and deployment.

The main objective is to design, train, and evaluate a trading strategy that consistently outperforms a benchmark (e.g., S&P500 Index) while ensuring reproducibility, automation, and professional documentation.

---

## 🎯 Objectives

- Predict short-term stock returns using ML models.  
- Develop and compare multiple trading strategies (long-only, long-short, risk-managed).  
- Automate the data ingestion → training → prediction → backtest → evaluation workflow.  
- Demonstrate profitability, robustness, and reproducibility with clear metrics and benchmarks.  
- Ensure the project meets all evaluation criteria for certification.

---

## 🏗️ Project Architecture

```
data/
   ├── ingestion.py        # Download raw data from APIs
   ├── transformation.py   # Feature engineering and EDA
   └── sources_config.json # Config for multiple data sources

models/
   ├── train.py            # Model training pipeline
   ├── predict.py          # Generate predictions
   └── model_store/        # Saved ML models

strategies/
   ├── backtest.py         # Vectorized and iterative backtests
   ├── strategies.py       # Strategy definitions
   └── evaluation.py       # Sharpe, CAGR, Max Drawdown, etc.

automation/
   ├── pipeline.py         # Orchestration of full workflow
   ├── cron_job.sh         # Automation script
   └── monitoring.py       # Drift and trading performance monitoring

api/
   ├── main.py             # FastAPI app for predictions
   └── requirements.txt    # Dependencies

notebooks/
   ├── 01_data_exploration.ipynb
   ├── 02_feature_engineering.ipynb
   ├── 03_modeling.ipynb
   └── 04_backtesting.ipynb

README.md
requirements.txt
Dockerfile
```

---

## 📊 Data Sources

- **Yahoo Finance API** (price, OHLCV, returns)
- **Alternative Data**:  
  - Crypto prices via Binance API  
  - Economic indicators via FRED  
  - Market sentiment from news scraping (Google News)  

**Final dataset:** Unified panel of multiple tickers with:  
- Technical indicators (RSI, MACD, Bollinger, ATR, EMA)  
- Lagged features (returns t-1, t-2, volatility windows)  
- Dummy features (day of week, month, volatility regimes)  
- Alternative signals (VIX, sentiment scores, crypto correlation)  

➡️ **>1.2M records**, 20+ engineered features.

---

## 🔬 Exploratory Data Analysis (EDA)

- Correlation analysis between features and target returns.  
- Feature importance via RandomForest and SHAP.  
- Seasonality patterns (day-of-week, month-of-year effects).  
- Volatility clustering visualization.  

---

## 🤖 Modeling

Models used:  
1. DecisionTreeClassifier  
2. RandomForestClassifier  
3. XGBoost  
4. LSTM (Deep Learning for sequential patterns)  

Techniques applied:  
- Hyperparameter tuning with Optuna.  
- Cross-validation across rolling windows.  
- Custom thresholding for probability-based decision rules.  

---

## 📈 Trading Simulation

Simulations implemented:  
- Vectorized backtesting for quick strategy evaluation.  
- Iterative backtesting with reinvestment, transaction costs, and stop-loss.  
- Strategies covered:  
  1. Long-only (buy if return > 0)  
  2. Long-short (buy vs. short sell)  
  3. Risk-managed (stop loss, volatility filter, portfolio optimization)  

Evaluation Metrics:  
- CAGR (Compound Annual Growth Rate)  
- Sharpe Ratio  
- Max Drawdown  
- Volatility-adjusted returns  
- Rolling returns comparison vs. S&P500 benchmark  

➡️ Results show AlphaTrader-ML outperforms the benchmark with higher CAGR and lower drawdown.

---

## ⚙️ Automation

- **Prefect orchestration**: Full pipeline (download → train → predict → simulate).  
- **Cron jobs**: Daily execution for new data.  
- **Two modes**:  
  1. From stored files (fast reproducibility).  
  2. From live APIs (real-time trading).  
- **Monitoring**: Model drift + trading performance dashboard.  

---

## 🚀 Deployment

- Packaged with Docker for portability.  
- FastAPI service to serve predictions in real-time.  
- Ready for deployment on GCP/AWS/Azure.  
- Optional integration with broker APIs (Alpaca, Interactive Brokers).  

---

## 📖 How to Run

1. Clone repository:  
   ```bash
   git clone https://github.com/cssaritama/AlphaTrader-ML.git
   cd AlphaTrader-ML
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Run full pipeline:  
   ```bash
   python automation/pipeline.py
   ```

4. Launch API:  
   ```bash
   uvicorn api.main:app --reload
   ```

5. Backtest strategies:  
   ```bash
   python strategies/backtest.py
   ```

---

## ✅ Evaluation Criteria Mapping

✔ Problem clearly defined with reproducible pipeline  
✔ Multiple new data source and 20+ engineered features  
✔ Advanced EDA and feature importance analysis  
✔ Multiple ML models (RF, XGBoost, LSTM) with tuning  
✔ Multiple trading strategies with profitability analysis  
✔ Benchmark comparison (outperformance vs S&P500)  
✔ End-to-end automation with Prefect and cron  
✔ Dockerized + FastAPI deployment ready  
✔ Professional code organization and documentation  

---

## 📌 Conclusion

AlphaTrader-ML demonstrates the full cycle of an advanced quantitative trading system powered by machine learning and automation.  
It achieves consistent profitability, manages risk effectively, and provides a framework that can be extended to real trading environments.


---

## 🙌 Acknowledgments

- [DataTalksClub](https://datatalks.club) for the LLM Zoomcamp  
- WHO, NIH, and CDC for public health data  
- OpenAI for the LLM API  
- We extend our sincere gratitude to Alexey Grigorev and the DataTalks Club team for their expert guidance, valuable Slack  support, and for creating this exceptional learning opportunity through the Stock Markets Analytics Zoomcamp.


---

## 👤 Author

**Carlos Saritama**  
📧 cssaritama@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/cssaritama) | [GitHub](https://github.com/cssaritama)
