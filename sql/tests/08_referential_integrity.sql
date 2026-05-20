-- dim_date to check whethere no orphaned rows, no missing dimension entries, no broken links between fact and dimension date table.
SELECT COUNT(*)
FROM fact_sales fs 
LEFT JOIN dim_date dd on dd.`date` = fs.`date` 
WHERE dd.`date`  IS NULL


-- dim_store to check whethere no orphaned rows, no missing dimension entries, no broken links between fact and dimension store table.
SELECT COUNT(*)
FROM fact_sales fs 
LEFT JOIN dim_store ds on ds.store_id  = fs.store_id 
where ds.store_id  IS NULL

-- dim_product to check whethere no orphaned rows, no missing dimension entries, no broken links between fact and dimension product table.

SELECT COUNT(*)
FROM fact_sales fs 
LEFT JOIN dim_product dp  ON dp.sku_id  = fs.sku_id 
WHERE dp.sku_id  IS NULL


-- dim_supplier to check whethere no orphaned rows, no missing dimension entries, no broken links between fact and dimension supplier table.


SELECT COUNT(*)
FROM fact_sales fs 
LEFT JOIN dim_supplier ds  ON ds.supplier_id  = fs.supplier_id 
WHERE ds.supplier_id IS NULL