# KPI alert rules from the project specification.
# Alerts are written to the pipeline log and to reports/alerts.txt.
# Email sending is included as an optional function: it only sends when
# ALERT_EMAIL and SMTP settings are provided as environment variables.


def check_alerts(monthly, headline, high_value_threshold=15000, min_monthly_revenue=10000):
    alerts = []

    # Rule 1: revenue drop more than 20% vs previous month
    if len(monthly) >= 2:
        last = monthly.iloc[-1]
        growth = last["revenue_growth_pct"]
        if growth is not None and growth < -20:
            alerts.append(f"ALERT: Revenue dropped {abs(growth)}% in {last['month']} (more than the 20% limit). Revenue is now Rs {last['total_revenue']:,.0f}.")

    # Rule 2: new high-value customer / very large single order value check is
    # done on total spend in main.py; here we check headline level
    if headline["total_revenue"] > 0 and headline["avg_order_value"] >= high_value_threshold:
        alerts.append(f"ALERT: Average order value is unusually high: Rs {headline['avg_order_value']:,.0f}.")

    # Rule 3: KPI below threshold - latest month revenue below minimum
    if len(monthly) >= 1:
        last = monthly.iloc[-1]
        if last["total_revenue"] < min_monthly_revenue:
            alerts.append(f"ALERT: Revenue in {last['month']} (Rs {last['total_revenue']:,.0f}) is below the minimum threshold of Rs {min_monthly_revenue:,.0f}.")

    return alerts


def check_high_value_customers(dim_customer, threshold=15000):
    alerts = []
    hv = dim_customer[dim_customer["total_spend"] >= threshold]
    for _, row in hv.iterrows():
        alerts.append(f"ALERT: High-value customer: {row['customer_name']} (ID {row['customer_id']}) total spend Rs {row['total_spend']:,.0f}.")
    return alerts
