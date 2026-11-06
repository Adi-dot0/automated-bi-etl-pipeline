import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformation.cleaning import clean_sales
from transformation.business_metrics import build_date_dimension, customer_segments


def sample_sales():
    return pd.DataFrame({
        "order_id": [1, 1, 2, 3],
        "customer_id": [1, 1, 1, 2],
        "product_id": [101, 101, 102, 101],
        "order_date": ["2026-08-01", "2026-08-01", "2026-08-02", "2026-08-03"],
        "quantity": [2, 2, -1, 1],
        "unit_price": [100, 100, 500, 100],
    })


def test_clean_sales_removes_duplicates_and_invalid():
    cleaned, report = clean_sales(sample_sales())
    assert report["duplicates_removed"] == 1
    assert report["invalid_removed"] == 1
    assert len(cleaned) == 2
    assert cleaned.iloc[0]["revenue"] == 200


def test_date_dimension():
    df = pd.DataFrame({"order_date": ["2026-08-01", "2026-08-01", "2026-09-02"]})
    dim = build_date_dimension(df)
    assert len(dim) == 2
    assert list(dim["month"]) == [8, 9]


def test_customer_segments():
    sales, _ = clean_sales(sample_sales())
    customers = pd.DataFrame({
        "customer_id": [1, 2], "customer_name": ["A", "B"], "city": ["X", "Y"],
        "email": ["a@x.com", "b@x.com"], "signup_date": ["2026-01-01", "2026-01-02"],
    })
    seg = customer_segments(sales, customers)
    assert seg.loc[seg["customer_id"] == 1, "total_orders"].iloc[0] == 1
