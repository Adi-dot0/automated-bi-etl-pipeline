# Automated Business Intelligence & ETL Pipeline

A Python ETL pipeline that takes raw sales, customer and product data, cleans and transforms it, loads it into a star-schema analytical warehouse, calculates business KPIs, checks alert rules, and exports fresh tables for a Power BI dashboard.

## Business Problem
Business data lives in different places — sales files, customer lists, product data. Analysts manually combine these sources, update reports and refresh dashboards, which creates delays and inconsistent reporting. This project automates that flow: one command runs the full extract → transform → load → KPI → alert cycle.

## What the pipeline does
1. **Extract** — reads sales orders, customers and products (CSV sources; `extraction/api_extractor.py` has the ready pattern for API sources with auth + pagination). Supports date-based filtering for incremental runs.
2. **Transform** — removes duplicates, drops invalid rows (missing/negative quantity, bad dates), calculates revenue, builds a date dimension, and segments customers (New / Regular / Premium by total spend).
3. **Load** — star schema warehouse: `fact_sales` + `dim_customer`, `dim_product`, `dim_date`, plus an `etl_execution_log` table that records every run.
4. **KPIs** — total revenue, total orders, average order value, repeat customers, monthly revenue and growth %, product revenue and share.
5. **Alerts** — revenue drop > 20% vs previous month, high-value customers, monthly revenue below threshold, pipeline failure logging.
6. **Power BI outputs** — every run refreshes CSV exports in `reports/` and the warehouse; see `power_bi/POWER_BI_GUIDE.md` to connect Power BI Desktop and build the dashboard.

## Tech Stack
Python, Pandas, SQL, SQLite (local warehouse — the same schema in `database/schema.sql` also runs on PostgreSQL), Power BI (dashboard layer, guide included), Apache Airflow (optional DAG template in `dags/`), GitHub

## Folder Structure
```
automated-bi-etl-pipeline/
  main.py
  requirements.txt
  README.md
  extraction/      file_extractor.py, api_extractor.py
  transformation/  cleaning.py, business_metrics.py
  loading/         database_loader.py
  database/        schema.sql, queries.sql
  monitoring/      etl_logger.py, alerts.py
  config/          config.json
  dags/            etl_dag.py (optional Airflow template)
  power_bi/        POWER_BI_GUIDE.md
  sample_data/     sales_orders.csv, customers.csv, products.csv
  reports/         kpi_monthly.csv, kpi_products.csv, fact/dim exports, alerts.txt, pipeline.log
  tests/           test_transformation.py, test_metrics.py
```

## How to Run
```bash
pip install -r requirements.txt
python main.py
```
Outputs: `data_warehouse.db` (SQLite warehouse), refreshed KPI/alert files in `reports/`, and a printed KPI summary.

## Verified Results (sample data)
Sample data is **clearly sample data** — 12 customers, 8 products, 63 sales rows for Aug–Oct 2026, with 4 problem rows added on purpose (2 duplicates, 1 missing quantity, 1 negative quantity).
- Extracted 63 sales rows → cleaning removed 2 duplicates + 2 invalid → **59 rows loaded into fact_sales**
- Total revenue: **Rs 1,74,500** | Total orders: **59** | Average order value: **Rs 2,957.63**
- Monthly revenue: Aug Rs 49,311 → Sep Rs 83,509 (+69.4%) → Oct Rs 41,680 (**-50.1%**)
- Alerts fired correctly: revenue-drop alert for Oct 2026, and 5 high-value customer alerts (spend ≥ Rs 15,000)
- Customer segments: Premium 8, Regular 3, New 1 | Repeat customers: 11 of 12
- Top product: Mechanical Keyboard — Rs 59,976 (34.4% of revenue)
- All **6 unit tests pass**; ETL execution log records the run as Success

## Tests
```bash
pip install pytest
pytest tests/ -v
```

## Limitations (honest)
- The warehouse runs on SQLite locally so the project works on any machine with no server setup. For a team setup, use the same schema on PostgreSQL (Power BI scheduled refresh then needs a gateway or a cloud database — see the Power BI guide).
- The Power BI dashboard is built by connecting Power BI Desktop to the pipeline outputs, following `power_bi/POWER_BI_GUIDE.md`. A .pbix file is not included because it must be created in Power BI Desktop.
- The API extractor is a ready template; the demo pipeline runs on the local sample files, not a live API.
- The Airflow DAG is a template for when Airflow is installed; scheduling also works with cron / Windows Task Scheduler.
- Alerts are written to the log and `reports/alerts.txt`. Email alert code is structured in `monitoring/alerts.py` design but sending needs your own SMTP settings via environment variables.
