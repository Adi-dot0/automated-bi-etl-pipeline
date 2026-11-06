# How to Run and Explain This Project

## Run it (Terminal, paste all 4 lines together)
```
git clone https://github.com/Adi-dot0/automated-bi-etl-pipeline.git
cd automated-bi-etl-pipeline
pip3 install -r requirements.txt
python3 main.py
```
If the clone says the folder already exists, skip line 1 and just do lines 2, 3, 4.
If pip gives an error, try: `pip3 install --user -r requirements.txt`

## What you should see (same numbers every time — the sample data is fixed)
- Headline KPIs: total_revenue 174500.0, total_orders 59, avg_order_value 2957.63
- Monthly: Aug 49,311 → Sep 83,509 → Oct 41,680
- Alerts: "Revenue dropped 50.1% in 2026-10" + 5 high-value customer alerts
- A file `data_warehouse.db` gets created, and the `reports/` files get refreshed

## Explain it in 5 steps (read the files in this order)
1. `extraction/file_extractor.py` — reads the 3 CSV files (sales, customers, products)
2. `transformation/cleaning.py` — removes duplicates and bad rows, adds a revenue column
3. `transformation/business_metrics.py` — monthly KPIs, customer segments, date table
4. `loading/database_loader.py` — saves everything into the warehouse tables
5. `monitoring/alerts.py` — checks the rules (revenue drop > 20%, high-value customers)
`main.py` just runs these 5 steps in order.

## Interview / viva one-liners
- **What is ETL?** Extract data from sources, Transform it (clean, calculate), Load it into a database for reporting.
- **What is a star schema?** One central fact table (fact_sales, the numbers) connected to dimension tables (customer, product, date — the details).
- **Fact vs dimension?** Fact = measurable events (orders, revenue). Dimension = the who/what/when around them.
- **How do alerts work?** After KPIs are calculated, rules are checked — for example, if this month's revenue is more than 20% lower than last month, an alert is written to the log.
- **Why SQLite here, PostgreSQL in teams?** SQLite needs no server, so the project runs anywhere. The same schema (database/schema.sql) runs on PostgreSQL for a shared team setup.
- **How does Power BI use this?** Power BI connects to the warehouse or to the refreshed CSV exports in reports/, so the dashboard shows new data after every pipeline run.
