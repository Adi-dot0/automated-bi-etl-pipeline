import pandas as pd


def build_date_dimension(sales_df):
    dates = pd.to_datetime(sales_df["order_date"]).drop_duplicates().sort_values()
    dim = pd.DataFrame({"date": dates.dt.strftime("%Y-%m-%d")})
    d = pd.to_datetime(dim["date"])
    dim["year"] = d.dt.year
    dim["month"] = d.dt.month
    dim["month_name"] = d.dt.strftime("%b")
    dim["day"] = d.dt.day
    dim["weekday"] = d.dt.strftime("%a")
    return dim


def customer_segments(sales_df, customers_df):
    spend = sales_df.groupby("customer_id").agg(
        total_orders=("order_id", "nunique"),
        total_spend=("revenue", "sum"),
        first_order=("order_date", "min"),
        last_order=("order_date", "max"),
    ).reset_index()

    def segment(x):
        if x >= 10000:
            return "Premium"
        if x >= 4000:
            return "Regular"
        return "New"

    spend["segment"] = spend["total_spend"].apply(segment)
    out = customers_df.merge(spend, on="customer_id", how="left")
    out["total_orders"] = out["total_orders"].fillna(0).astype(int)
    out["total_spend"] = out["total_spend"].fillna(0)
    out["segment"] = out["segment"].fillna("No Orders")
    return out


def monthly_kpis(sales_df):
    df = sales_df.copy()
    df["month"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m")
    kpi = df.groupby("month").agg(
        total_orders=("order_id", "nunique"),
        total_revenue=("revenue", "sum"),
        total_quantity=("quantity", "sum"),
        unique_customers=("customer_id", "nunique"),
    ).reset_index()
    kpi["avg_order_value"] = (kpi["total_revenue"] / kpi["total_orders"]).round(2)
    kpi["revenue_growth_pct"] = (kpi["total_revenue"].pct_change() * 100).round(1)
    return kpi


def product_kpis(sales_df, products_df):
    p = sales_df.groupby("product_id").agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
    ).reset_index()
    p = p.merge(products_df[["product_id", "product_name", "category"]], on="product_id", how="left")
    p = p.sort_values("total_revenue", ascending=False)
    total = p["total_revenue"].sum()
    p["revenue_share_pct"] = (p["total_revenue"] / total * 100).round(1) if total else 0
    return p


def headline_kpis(sales_df, customers_df):
    total_revenue = float(sales_df["revenue"].sum())
    total_orders = int(sales_df["order_id"].nunique())
    return {
        "total_revenue": round(total_revenue, 2),
        "total_orders": total_orders,
        "avg_order_value": round(total_revenue / total_orders, 2) if total_orders else 0,
        "total_customers_with_orders": int(sales_df["customer_id"].nunique()),
        "total_customers": int(customers_df["customer_id"].nunique()),
        "repeat_customers": int((sales_df.groupby("customer_id")["order_id"].nunique() > 1).sum()),
    }
