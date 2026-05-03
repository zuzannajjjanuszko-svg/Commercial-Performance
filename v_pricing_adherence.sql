-- Pricing Adherence (contracts with discount ≤ policy threshold)
CREATE VIEW v_pricing_adherence AS
SELECT 
    contract_id,
    client_id,
    product_id,
    contracted_monthly_revenue,
    discount_pct,
    CASE WHEN discount_pct IS NULL THEN 'Missing'
         WHEN discount_pct <= 10 THEN 'Adherent'
         ELSE 'Non-Adherent' END AS adherence_flag,
    CASE WHEN discount_pct > 10 THEN contracted_monthly_revenue * discount_pct / 100.0
         ELSE 0 END AS estimated_leakage_monthly
FROM fact_contracts;