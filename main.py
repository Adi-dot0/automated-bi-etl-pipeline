import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from extraction.file_extractor import extract_all
from transformation.cleaning import clean_sales, clean_customers, clean_products
from transformation.business_metrics import build_date_dimension, customer_segments, monthly_kpis, product_kpis, headline_kpis
from loading.database_loader import load_tables, log_execution
from monitoring.etl_logger import get_logger
from monitoring.alerts import check_alerts, check_high_value_customers

BASE = os.path.dirname(__file__)
PIPELINE_NAME = "automated-bi-etl-pipeline"


def run_pipeline(start_date=None):
    logger = get_logger()
    start = datetime.now()
    logger.info(f"Pipeline started: {PIPELINE_NAME} at {start.strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # 1. Extract
        data = extract_all(start_date=start_date)
        logger.info(f"Extracted: sales={len(data['sales'])}, customers={len(data['customers'])}, products={len(data['products'])}")

        # 2. Transform
        sales, clean_report = clean_sales(data["sales"])
        customers = clean_customers(data["customers"])
        products = clean_products(data["products"])
        logger.info(f"Cleaning sales: {clean_report}")

        dim_date = build_date_dimension(sales)
        dim_customer = customer_segments(sales, customers)
        fact_sales = sales[["order_id", "customer_id", "product_id", "order_date", "quantity", "revenue"]].copy()

        # 3. Load (star schema warehouse)
        loaded = load_tables(fact_sales, dim_customer, products, dim_date)
        logger.info(f"Loaded {loaded} rows into fact_sales")

        # 4. KPIs
        headline = headline_kpis(sales, customers)
        monthly = monthly_kpis(sales)
        products_kpi = product_kpis(sales, products)

        # 5. Alerts
        alerts = check_alerts(monthly, headline)
        alerts += check_high_value_customers(dim_customer)
        for a in alerts:
            logger.warning(a)

        # 6. Reports for Power BI / sharing (refreshed every run)
        reports_dir = os.path.join(BASE, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        monthly.to_csv(os.path.join(reports_dir, "kpi_monthly.csv"), index=False)
        products_kpi.to_csv(os.path.join(reports_dir, "kpi_products.csv"), index=False)
        dim_customer.to_csv(os.path.join(reports_dir, "dim_customer_export.csv"), index=False)
        fact_sales.to_csv(os.path.join(reports_dir, "fact_sales_export.csv"), index=False)
        with open(os.path.join(reports_dir, "alerts.txt"), "w") as f:
            f.write("\n".join(alerts) if alerts else "No alerts in this run.")

        end = datetime.now()
        log_execution(PIPELINE_NAME, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), loaded, "Success")
        logger.info(f"Pipeline finished successfully in {(end - start).total_seconds():.1f} seconds")

        print("\n--- HEADLINE KPIs ---")
        for k, v in headline.items():
            print(f"{k}: {v}")
        print("\n--- MONTHLY KPIs ---")
        print(monthly.to_string(index=False))
        print("\n--- TOP PRODUCTS ---")
        print(products_kpi.head(5).to_string(index=False))
        print("\n--- ALERTS ---")
        print("\n".join(alerts) if alerts else "No alerts")
        return {"headline": headline, "monthly": monthly, "alerts": alerts, "clean_report": clean_report, "loaded": loaded}

    except Exception as e:
        end = datetime.now()
        log_execution(PIPELINE_NAME, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), 0, "Failed", str(e))
        logger.error(f"Pipeline FAILED: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()
