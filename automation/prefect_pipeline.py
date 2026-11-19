#**Author:** Carlos Stalin Saritama Atopo  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 


"""
prefect_pipeline.py

Simple Prefect flow to orchestrate the pipeline.
"""
from prefect import task, Flow
import subprocess
import sys

@task
def data_task():
    subprocess.run([sys.executable, "scripts/data_collection.py", "--use-sample"], check=True)

@task
def feature_task():
    subprocess.run([sys.executable, "scripts/feature_engineering.py"], check=True)

@task
def train_task():
    subprocess.run([sys.executable, "scripts/model_training.py"], check=True)

@task
def sim_task():
    subprocess.run([sys.executable, "scripts/trading_simulation.py"], check=True)

with Flow("algo-trading-pipeline") as flow:
    d = data_task()
    f = feature_task(upstream_tasks=[d])
    t = train_task(upstream_tasks=[f])
    s = sim_task(upstream_tasks=[t])

if __name__ == "__main__":
    flow.run()