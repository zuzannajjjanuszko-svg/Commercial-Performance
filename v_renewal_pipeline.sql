-- Renewal Pipeline (contracts expiring in next 90 days)
CREATE VIEW v_renewal_pipeline AS
SELECT 
    ct.contract_id,
    cl.client_name,
    pr.product_name,
    ct.contracted_monthly_revenue,
    ct.end_date,
    ct.sales_rep,
    CASE WHEN ct.end_date < CURRENT_DATE THEN 'Expired'
         WHEN ct.end_date <= CURRENT_DATE + INTERVAL '90 days' THEN 'At Risk'
         ELSE 'Active' END AS renewal_status
FROM fact_contracts ct
JOIN dim_clients cl ON ct.client_id = cl.client_id
JOIN dim_products pr ON ct.product_id = pr.product_id
WHERE ct.end_date IS NOT NULL;