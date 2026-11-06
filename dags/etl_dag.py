# Optional Apache Airflow DAG - template only.
# Use this when Airflow is installed: copy this file into your Airflow
# dags folder and the pipeline will run daily. It is not required for
# running the project with `python main.py` or Windows Task Scheduler / cron.

from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:
    DAG = None

import os
import sys

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)


def run():
    from main import run_pipeline
    run_pipeline()


if DAG is not None:
    with DAG(
        dag_id="automated_bi_etl_pipeline",
        start_date=datetime(2026, 11, 1),
        schedule="@daily",
        catchup=False,
        default_args={"retries": 1, "retry_delay": timedelta(minutes=5)},
        description="Daily ETL: extract sales data, transform, load star schema warehouse, check KPI alerts",
    ) as dag:
        PythonOperator(task_id="run_etl_pipeline", python_callable=run)
