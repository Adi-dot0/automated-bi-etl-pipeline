import pandas as pd


def clean_sales(df):
    report = {}
    report["rows_in"] = len(df)

    df = df.copy()
    df = df.drop_duplicates()
    report["duplicates_removed"] = report["rows_in"] - len(df)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    before = len(df)
    # rows that cannot be used: missing/invalid quantity, price or date, or quantity <= 0
    df = df.dropna(subset=["quantity", "unit_price", "order_date"])
    df = df[df["quantity"] > 0]
    report["invalid_removed"] = before - len(df)

    df["quantity"] = df["quantity"].astype(int)
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    report["rows_out"] = len(df)
    return df, report


def clean_customers(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["customer_id"])
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df


def clean_products(df):
    df = df.copy()
    df = df.drop_duplicates(subset=["product_id"])
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    return df
