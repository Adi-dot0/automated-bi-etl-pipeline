import pandas as pd
import os

SAMPLE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sample_data")


def extract_csv(filename, start_date=None):
    path = os.path.join(SAMPLE_DIR, filename)
    df = pd.read_csv(path)
    # date based filtering (used for incremental runs)
    if start_date and "order_date" in df.columns:
        df = df[pd.to_datetime(df["order_date"], errors="coerce") >= pd.to_datetime(start_date)]
    return df


def extract_all(start_date=None):
    data = {}
    data["sales"] = extract_csv("sales_orders.csv", start_date=start_date)
    data["customers"] = extract_csv("customers.csv")
    data["products"] = extract_csv("products.csv")
    return data
