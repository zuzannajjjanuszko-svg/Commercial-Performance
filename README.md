# Commercial Performance Dashboard

A commercial analytics project built to demonstrate SQL (PostgreSQL) and Power BI skills for financial operations roles. The dashboard tracks revenue attainment, pricing adherence, revenue leakage, and data quality.
## Live Dashboards

[Commercial Performance Dashboard (SQL Views)](https://app.powerbi.com/view?r=eyJrIjoiODIxNjY2Y2YtYWIwZC00ZjBmLTliMzgtZGFmYzUxNmUwNGI2IiwidCI6ImE2ZTRmMjUxLTE4ZDYtNDJiMS04ZmY1LTZlYTg1MDhhZjg3MSJ9&embedImagePlaceholder=true)

[Commercial Performance Dashboard (Base Tables)](https://app.powerbi.com/view?r=eyJrIjoiMTkxOWZiOTItMmMyMS00NzY5LWE0ZGItNjU2NmUwYzQzZTg2IiwidCI6ImE2ZTRmMjUxLTE4ZDYtNDJiMS04ZmY1LTZlYTg1MDhhZjg3MSJ9&embedImagePlaceholder=true)

## Architecture

- **SQL** — Business logic defined in PostgreSQL views (pricing adherence, revenue attainment, NRR, renewal pipeline, data quality checks)
- **Python** — Simulated realistic B2B financial data generation (pandas), CSV export, data cleaning
- **Power BI** — Star schema model, DAX measures, multi-page interactive report

## Repository Structure

- `/sql` — SQL view definitions
- `/python` — Data generation, export, and cleaning scripts
- `/data` — CSV exports from the SQL views and base tables
- `/powerbi` — Power BI report files

## Skills Demonstrated

- SQL: window functions, CTEs, CASE logic, data quality checks, view creation
- Power BI: star schema modeling, DAX measures (revenue, targets, attainment, leakage), report design
- Python: data generation with pandas, file export, data cleaning

## About the Project

This project was built from scratch to simulate a commercial performance monitoring system for a B2B financial information company or other similar companies.
