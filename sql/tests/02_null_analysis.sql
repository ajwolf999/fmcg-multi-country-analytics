-- Test: Null Analysis
-- Expected: if there are missng values
-- Result: PASS
-- Notes: Zero nulls across all 18 columns checked. Synthetically clean dataset.
SELECT
    SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END)           AS null_date,
    SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END)       AS null_store_id,
    SUM(CASE WHEN country IS NULL THEN 1 ELSE 0 END)        AS null_country,
    SUM(CASE WHEN sku_id IS NULL THEN 1 ELSE 0 END)         AS null_sku_id,
    SUM(CASE WHEN category IS NULL THEN 1 ELSE 0 END)       AS null_category,
    SUM(CASE WHEN units_sold IS NULL THEN 1 ELSE 0 END)     AS null_units_sold,
    SUM(CASE WHEN gross_sales IS NULL THEN 1 ELSE 0 END)    AS null_gross_sales,
    SUM(CASE WHEN net_sales IS NULL THEN 1 ELSE 0 END)      AS null_net_sales,
    SUM(CASE WHEN list_price IS NULL THEN 1 ELSE 0 END)     AS null_list_price,
    SUM(CASE WHEN discount_pct IS NULL THEN 1 ELSE 0 END)   AS null_discount_pct,
    SUM(CASE WHEN promo_flag IS NULL THEN 1 ELSE 0 END)     AS null_promo_flag,
    SUM(CASE WHEN stock_on_hand IS NULL THEN 1 ELSE 0 END)  AS null_stock_on_hand,
    SUM(CASE WHEN stock_out_flag IS NULL THEN 1 ELSE 0 END) AS null_stock_out_flag,
    SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END)    AS null_temperature,
    SUM(CASE WHEN rain_mm IS NULL THEN 1 ELSE 0 END)        AS null_rain_mm,
    SUM(CASE WHEN margin_pct IS NULL THEN 1 ELSE 0 END)     AS null_margin_pct,
    SUM(CASE WHEN purchase_cost IS NULL THEN 1 ELSE 0 END)  AS null_purchase_cost,
    SUM(CASE WHEN supplier_id IS NULL THEN 1 ELSE 0 END)    AS null_supplier_id
FROM raw_sales;