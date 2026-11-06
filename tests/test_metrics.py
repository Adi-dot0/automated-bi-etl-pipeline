import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from transformation.business_metrics import monthly_kpis, headline_kpis
from monitoring.alerts import check_alerts


def sales_df():
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "customer_id": [1, 1, 2],
        "product_id": [101, 102, 101],
        "order_date": ["2026-08-05", "2026-09-05", "2026-09-06"],
        "quantity": [1, 2, 1],
        "revenue": [1000.0, 400.0, 100.0],
    })


def test_monthly_kpis_growth():
    kpi = monthly_kpis(sales_df())
    assert len(kpi) == 2
    aug = kpi[kpi["month"] == "2026-08"].iloc[0]
    assert aug["total_revenue"] == 1000
    sep = kpi[kpi["month"] == "2026-09"].iloc[0]
    assert sep["revenue_growth_pct"] == -50.0


def test_headline_kpis():
    customers = pd.DataFrame({"customer_id": [1, 2, 3]})
    h = headline_kpis(sales_df(), customers)
    assert h["total_revenue"] == 1500
    assert h["total_orders"] == 3
    assert h["repeat_customers"] == 1


def test_revenue_drop_alert():
    kpi = monthly_kpis(sales_df())
    h = headline_kpis(sales_df(), pd.DataFrame({"customer_id": [1, 2]}))
    alerts = check_alerts(kpi, h, min_monthly_revenue=0)
    assert any("dropped" in a for a in alerts)
