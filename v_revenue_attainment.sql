-- Revenue Attainment by Region & Month
CREATE VIEW v_revenue_attainment AS
SELECT 
    t.region,
    t.month_date,
    SUM(t.revenue_target) AS target_revenue,
    COALESCE(SUM(ra.recognized_revenue), 0) AS actual_revenue,
    ROUND(COALESCE(SUM(ra.recognized_revenue), 0) / NULLIF(SUM(t.revenue_target), 0) * 100, 1) AS attainment_pct
FROM fact_targets t
LEFT JOIN dim_clients c ON t.region = c.region
LEFT JOIN fact_contracts ct ON c.client_id = ct.client_id AND t.product_id = ct.product_id
LEFT JOIN fact_revenue_actuals ra ON ct.contract_id = ra.contract_id 
    AND DATE_TRUNC('month', ra.month_date) = DATE_TRUNC('month', t.month_date)
GROUP BY t.region, t.month_date;
