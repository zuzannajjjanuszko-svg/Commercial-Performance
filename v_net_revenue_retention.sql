-- Net Revenue Retention (12 months trailing)
CREATE VIEW v_net_revenue_retention AS
WITH monthly_cohort AS (
    SELECT 
        ct.contract_id,
        DATE_TRUNC('month', ra.month_date) AS month,
        SUM(ra.recognized_revenue) AS revenue
    FROM fact_contracts ct
    JOIN fact_revenue_actuals ra ON ct.contract_id = ra.contract_id
    GROUP BY ct.contract_id, DATE_TRUNC('month', ra.month_date)
),
lagged AS (
    SELECT 
        contract_id,
        month,
        revenue,
        LAG(revenue, 12) OVER (PARTITION BY contract_id ORDER BY month) AS revenue_12m_ago
    FROM monthly_cohort
)
SELECT 
    month,
    SUM(revenue) AS total_revenue,
    SUM(revenue_12m_ago) AS baseline_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(revenue_12m_ago), 0) * 100, 1) AS nrr_pct
FROM lagged
WHERE revenue_12m_ago IS NOT NULL
GROUP BY month;