import sqlite3
import os

BASE = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE, "data_warehouse.db")
SCHEMA = os.path.join(BASE, "database", "schema.sql")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA) as f:
        conn.executescript(f.read())
    return conn


def load_tables(fact_sales, dim_customer, dim_product, dim_date):
    conn = get_connection()
    # full refresh of the analytical tables each run (small data, simple and safe)
    fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)
    dim_customer.to_sql("dim_customer", conn, if_exists="replace", index=False)
    dim_product.to_sql("dim_product", conn, if_exists="replace", index=False)
    dim_date.to_sql("dim_date", conn, if_exists="replace", index=False)
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM fact_sales").fetchone()[0]
    conn.close()
    return count


def log_execution(pipeline_name, start_time, end_time, records, status, error=""):
    conn = get_connection()
    conn.execute(
        "INSERT INTO etl_execution_log (pipeline_name, start_time, end_time, records_processed, execution_status, error_message) VALUES (?, ?, ?, ?, ?, ?)",
        (pipeline_name, start_time, end_time, records, status, error),
    )
    conn.commit()
    conn.close()
