# Power BI Dashboard Guide

The ETL pipeline refreshes the warehouse and the export files on every run.
Power BI connects to those outputs — so when the pipeline runs, the dashboard data is new.

## Option A — Connect Power BI Desktop to the export files (easiest, no gateway)
1. Run the pipeline: `python main.py`
2. Open Power BI Desktop → Get Data → Text/CSV
3. Load these files from the `reports/` folder:
   - fact_sales_export.csv (fact table)
   - dim_customer_export.csv (customer dimension, with segment)
   - kpi_monthly.csv, kpi_products.csv (ready KPI tables)
4. Build the visuals below, then Publish.

## Option B — Connect to the database
- Local: the warehouse is SQLite (`data_warehouse.db`). Power BI connects to SQLite through an ODBC driver.
- Team setup: run the same schema on PostgreSQL (`database/schema.sql` works on PostgreSQL) and use Power BI's PostgreSQL connector. Scheduled refresh in Power BI Service then needs a gateway for an on-premises database, or a cloud database — this depends on your licence and setup.

## Dashboard visuals (from the project specification)
**Sales KPIs:** Total Revenue (card), Total Orders (card), Average Order Value (card), Monthly Revenue + Growth % (line/column chart from kpi_monthly.csv)
**Customer KPIs:** Customers by Segment (donut, dim_customer.segment), New vs Repeat Customers (from fact_sales: customers with 1 order vs more than 1), Top Cities by Revenue (bar, join fact_sales + dim_customer)
**Product KPIs:** Top Products by Revenue (bar, kpi_products.csv), Revenue Share % by Product, Category Performance (bar)

## Refresh
- Manual: run `python main.py`, then Refresh in Power BI Desktop.
- Scheduled: schedule main.py daily (cron / Task Scheduler, or the Airflow DAG in `dags/`), and set a scheduled refresh in Power BI Service for the published dataset. Power BI data alerts can then be set on the published dashboard cards (for example revenue drop) — alerts work only on supported dashboard tiles in Power BI Service.
