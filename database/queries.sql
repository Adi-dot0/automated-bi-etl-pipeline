-- KPI queries for the Power BI dashboard and the pipeline report.
-- These run on the warehouse tables (fact_sales, dim_customer, dim_product, dim_date).

-- 1. Monthly revenue and orders
SELECT substr(order_date, 1, 7) AS month,
       COUNT(DISTINCT order_id) AS total_orders,
       SUM(revenue) AS total_revenue,
       ROUND(SUM(revenue) * 1.0 / COUNT(DISTINCT order_id), 2) AS avg_order_value
FROM fact_sales
GROUP BY month
ORDER BY month;

-- 2. Top selling products by revenue
SELECT p.product_name, p.category,
       COUNT(DISTINCT f.order_id) AS total_orders,
       SUM(f.quantity) AS total_quantity,
       SUM(f.revenue) AS total_revenue
FROM fact_sales f
JOIN dim_product p ON p.product_id = f.product_id
GROUP BY p.product_name, p.category
ORDER BY total_revenue DESC;

-- 3. Revenue by customer segment
SELECT segment, COUNT(*) AS customers, SUM(total_spend) AS segment_revenue
FROM dim_customer
GROUP BY segment
ORDER BY segment_revenue DESC;

-- 4. Revenue by city
SELECT c.city, SUM(f.revenue) AS total_revenue, COUNT(DISTINCT f.order_id) AS total_orders
FROM fact_sales f
JOIN dim_customer c ON c.customer_id = f.customer_id
GROUP BY c.city
ORDER BY total_revenue DESC;
