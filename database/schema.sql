-- Star schema for the analytical warehouse.
-- Written in standard SQL: runs on SQLite (used locally in this project)
-- and on PostgreSQL with the same table design.

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id   INTEGER PRIMARY KEY,
    customer_name TEXT,
    city          TEXT,
    email         TEXT,
    signup_date   TEXT,
    segment       TEXT,
    total_orders  INTEGER,
    total_spend   REAL
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id   INTEGER PRIMARY KEY,
    product_name TEXT,
    category     TEXT,
    unit_price   REAL
);

CREATE TABLE IF NOT EXISTS dim_date (
    date       TEXT PRIMARY KEY,
    year       INTEGER,
    month      INTEGER,
    month_name TEXT,
    day        INTEGER,
    weekday    TEXT
);

CREATE TABLE IF NOT EXISTS fact_sales (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id  INTEGER,
    order_date  TEXT,
    quantity    INTEGER,
    revenue     REAL,
    FOREIGN KEY (customer_id) REFERENCES dim_customer (customer_id),
    FOREIGN KEY (product_id) REFERENCES dim_product (product_id),
    FOREIGN KEY (order_date) REFERENCES dim_date (date)
);

CREATE TABLE IF NOT EXISTS etl_execution_log (
    execution_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_name     TEXT,
    start_time        TEXT,
    end_time          TEXT,
    records_processed INTEGER,
    execution_status  TEXT,
    error_message     TEXT
);
