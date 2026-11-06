from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

OUT = "Automated_BI_ETL_Pipeline_Project_Report.pdf"
styles = getSampleStyleSheet()
title = ParagraphStyle("title2", parent=styles["Title"], fontSize=22, leading=28)
subtitle = ParagraphStyle("sub", parent=title, fontSize=15, leading=20)
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=15, spaceBefore=14, spaceAfter=6, textColor=colors.HexColor("#1F3864"))
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=12.5, spaceBefore=10, spaceAfter=4)
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=11, leading=15.5, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle("bullet", parent=body, alignment=0, leftIndent=14, spaceAfter=3)
center = ParagraphStyle("center", parent=body, alignment=TA_CENTER)
mono = ParagraphStyle("mono", parent=styles["Code"], fontSize=9.5, leading=13, leftIndent=10, spaceAfter=6)

def P(t, s=body): return Paragraph(t, s)
def bullets(items): return [P(f"- {i}", bullet) for i in items]
def make_table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1F3864")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),0.5,colors.grey),("FONTSIZE",(0,0),(-1,-1),10.5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
    return t

story = []
story.append(Spacer(1, 3*cm))
story.append(P("PROJECT REPORT", title)); story.append(Spacer(1, 0.5*cm))
story.append(P("Automated Business Intelligence &amp; Dashboard Refresh Pipeline", subtitle))
story.append(Spacer(1, 1.2*cm))
story.append(P("Submitted by: <b>Aditya Mishra</b>", center))
story.append(P("BCA Student, Lovely Professional University (Expected 2027)", center))
story.append(P("Date: 6 November 2026", center)); story.append(Spacer(1, 1*cm))
story.append(P("GitHub Repository: https://github.com/Adi-dot0/automated-bi-etl-pipeline", center))
story.append(PageBreak())

story.append(P("1. Abstract", h1))
story.append(P("This project is an automated ETL (Extract, Transform, Load) pipeline in Python that prepares business data for Business Intelligence reporting. It extracts sales, customer and product data, cleans and transforms it, loads it into a star-schema analytical warehouse, calculates sales, customer and product KPIs, checks alert rules such as a revenue drop of more than 20 percent, and exports fresh Power BI-ready tables on every run. On the sample dataset provided with the project, the pipeline processed 63 raw sales rows, removed 2 duplicates and 2 invalid rows, loaded 59 clean orders worth Rs 1,74,500 in total revenue, and correctly raised a revenue-drop alert for October 2026."))

story.append(P("2. Business Problem", h1))
story.append(P("Businesses collect data in many places: Excel spreadsheets, CRM systems, databases and sales platforms. Analysts manually combine these sources, clean them, update reports and refresh dashboards. This creates delays, inconsistent reporting and repeated manual effort. A centralized automated pipeline removes this repeated work and makes the same clean, updated data available for every dashboard refresh."))

story.append(P("3. Objectives", h1))
story.extend(bullets([
    "Extract business data from file sources, with a ready pattern for API sources",
    "Transform data: cleaning, revenue calculation, customer segmentation and a date dimension",
    "Load data into a star-schema warehouse (one fact table and dimension tables)",
    "Calculate sales, customer and product KPIs automatically on every run",
    "Raise alerts for important changes such as a revenue drop of more than 20 percent",
    "Log every pipeline run so failures can be traced",
    "Export refreshed tables that a Power BI dashboard can connect to",
]))

story.append(P("4. Technology Stack", h1))
story.append(make_table([
    ["Tool", "Use in this project"],
    ["Python", "ETL automation"],
    ["Pandas", "Data extraction and transformation"],
    ["SQL", "Warehouse schema and KPI queries (database/schema.sql, queries.sql)"],
    ["SQLite", "Local analytical warehouse (same schema also runs on PostgreSQL)"],
    ["Power BI", "Dashboard layer - connects to the pipeline outputs (guide in power_bi folder)"],
    ["Apache Airflow", "Optional scheduling - DAG template provided in dags folder"],
    ["Requests", "API extraction pattern (extraction/api_extractor.py)"],
    ["GitHub", "Version control and project hosting"],
], [4*cm, 11*cm]))

story.append(P("5. System Architecture", h1))
story.append(P("Data Sources (CSV / API) &rarr; Python Extraction &rarr; Data Validation and Cleaning &rarr; Transformation (Python + SQL) &rarr; Star-Schema Warehouse &rarr; KPI Calculation &rarr; Alerts + Power BI-Ready Exports &rarr; Power BI Dashboard", ParagraphStyle("flow", parent=body, alignment=TA_CENTER)))

story.append(P("6. Modules of the System", h1))
story.append(P("Module 1 - Data Extraction (extraction/)", h2))
story.append(P("file_extractor.py reads the sales, customer and product CSV files and supports date-based filtering for incremental runs. api_extractor.py provides the API pattern from the specification: authorization header, pagination and error handling, ready to connect to a real CRM or product API."))
story.append(P("Module 2 - Data Transformation (transformation/)", h2))
story.append(P("cleaning.py removes duplicate orders and drops invalid rows (missing or negative quantity, invalid dates), converts data types and calculates revenue as quantity multiplied by unit price. business_metrics.py builds the date dimension (year, month, weekday), segments customers as New, Regular or Premium based on total spend, and calculates monthly KPIs, product KPIs and headline KPIs."))
story.append(P("Module 3 - Database Loading (loading/database_loader.py)", h2))
story.append(P("Creates the warehouse from database/schema.sql and loads the star schema: fact_sales (order_id, customer_id, product_id, order_date, quantity, revenue) with dim_customer, dim_product and dim_date dimension tables. Every run is also recorded in etl_execution_log with start and end time, records processed and status."))
story.append(P("Module 4 - KPI Monitoring (transformation/business_metrics.py + database/queries.sql)", h2))
story.append(P("Sales KPIs: total revenue, total orders, average order value, monthly revenue growth. Customer KPIs: total and repeat customers, customer segments. Product KPIs: top products by revenue and revenue share. The same KPIs are also written as SQL queries in database/queries.sql for use inside the warehouse or a BI tool."))
story.append(P("Module 5 - Automated Alerts (monitoring/alerts.py)", h2))
story.append(P("Rules: revenue drop of more than 20 percent compared to the previous month; a high-value customer whose total spend crosses the threshold in config; monthly revenue below a minimum threshold; and pipeline failure, which is recorded in the execution log and the pipeline log file. Alerts are written to reports/alerts.txt on every run."))
story.append(P("Module 6 - Dashboard Refresh (reports/ exports + power_bi guide)", h2))
story.append(P("Every pipeline run refreshes the warehouse and the export files (fact_sales, dim_customer, KPI tables). Power BI Desktop connects to these outputs, so a dashboard built on them shows new data after each run. Scheduled refresh in Power BI Service depends on the dataset type, licence and gateway requirements, as noted in the specification; the guide in the power_bi folder explains both the file connection and the database connection options."))

story.append(P("7. How to Run the Project", h1))
story.append(P("pip install -r requirements.txt", mono))
story.append(P("python main.py", mono))
story.append(P("The pipeline prints the headline KPIs, monthly KPIs, top products and any alerts, writes the warehouse file data_warehouse.db, and refreshes all report files in the reports folder.", body))

story.append(P("8. Testing and Results", h1))
story.append(P("Unit tests", h2))
story.append(P("Six unit tests in the tests folder cover sales cleaning (duplicates and invalid rows), the date dimension, customer segmentation, monthly KPI growth calculation, headline KPIs and the revenue-drop alert rule. All 6 tests pass."))
story.append(P("Results on sample data", h2))
story.append(P("The sample data (sample_data folder) contains 12 customers, 8 products and 63 sales rows for August to October 2026, with 4 problem rows added on purpose: 2 duplicate orders, 1 row with a missing quantity and 1 row with a negative quantity. Verified results:", body))
story.append(make_table([
    ["Measure", "Result"],
    ["Sales rows extracted", "63"],
    ["Duplicates removed", "2"],
    ["Invalid rows removed", "2"],
    ["Rows loaded in fact_sales", "59"],
    ["Total revenue", "Rs 1,74,500"],
    ["Total orders", "59"],
    ["Average order value", "Rs 2,957.63"],
    ["Repeat customers", "11 out of 12"],
    ["Customer segments", "Premium 8, Regular 3, New 1"],
    ["Top product", "Mechanical Keyboard - Rs 59,976 (34.4% of revenue)"],
], [6*cm, 9*cm]))
story.append(P("Monthly revenue: August Rs 49,311, September Rs 83,509 (growth +69.4 percent), October Rs 41,680 (growth -50.1 percent). Because October revenue fell by more than 20 percent, the revenue-drop alert fired correctly, and 5 high-value customer alerts were raised for customers with total spend of Rs 15,000 or more. The etl_execution_log recorded the run as Success with 59 records processed.", body))

story.append(P("9. Limitations", h1))
story.extend(bullets([
    "The warehouse runs on SQLite locally so the project works on any machine without a server; the same schema is provided for PostgreSQL for a team setup",
    "A Power BI .pbix file is not included because it must be created in Power BI Desktop; the project provides the refreshed data and a step-by-step connection guide instead",
    "The API extractor is a ready template; the demonstration pipeline runs on the local sample files, not a live API",
    "The Airflow DAG is a template for when Airflow is installed; scheduling also works with cron or Windows Task Scheduler",
    "Alerts are written to the log and a text file; sending email alerts needs the user's own SMTP settings",
]))

story.append(P("10. Future Scope", h1))
story.append(P("Connect a real data source through the API extractor, move the warehouse to PostgreSQL, build the Power BI dashboard from the provided guide and publish it with scheduled refresh, and add the third portfolio project (Automated Web Scraping and CRM Synchronization with HubSpot).", body))

story.append(P("11. Conclusion", h1))
story.append(P("The pipeline automates the complete path from raw business files to dashboard-ready data: extraction, cleaning, transformation, star-schema loading, KPI calculation, alert checking and run logging happen in a single command. Testing on sample data with known problems showed correct cleaning (59 of 63 rows loaded), correct KPI values verified both in Python and with SQL queries on the warehouse, and correct alert behaviour. The complete project is available on GitHub at https://github.com/Adi-dot0/automated-bi-etl-pipeline", body))

story.append(P("Appendix - Project Files", h1))
story.append(P("main.py; extraction/file_extractor.py and api_extractor.py; transformation/cleaning.py and business_metrics.py; loading/database_loader.py; database/schema.sql and queries.sql; monitoring/etl_logger.py and alerts.py; config/config.json; dags/etl_dag.py; power_bi/POWER_BI_GUIDE.md; sample_data (3 CSV files); reports (KPI tables, exports, alerts); tests/test_transformation.py and test_metrics.py; requirements.txt; README.md.", body))

doc = SimpleDocTemplate(OUT, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm,
                        title="Project Report - Automated BI & ETL Pipeline", author="Aditya Mishra")
doc.build(story)
print("built", OUT)
