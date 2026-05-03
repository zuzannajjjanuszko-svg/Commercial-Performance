-- Data Quality Checks
CREATE VIEW v_data_quality_flags AS
SELECT 'Missing Discount' AS issue_type, contract_id::TEXT AS identifier 
FROM fact_contracts WHERE discount_pct IS NULL
UNION ALL
SELECT 'Negative Revenue' AS issue_type, revenue_id::TEXT 
FROM fact_revenue_actuals WHERE recognized_revenue < 0
UNION ALL
SELECT 'Duplicate Revenue' AS issue_type, CONCAT(contract_id::TEXT, '-', month_date::TEXT)
FROM fact_revenue_actuals
GROUP BY contract_id, month_date
HAVING COUNT(*) > 1;