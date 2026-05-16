-- Test: Dataset shape and coverage
-- Expected: 1.1M rows, 7 countries, 3-year date range
-- Result: PASS
-- Notes: Thin store/city coverage (13 stores, 9 cities across 7 countries)
--        suggests synthetic/sample dataset. Analysis valid at store level,
--        not representative of full country markets.
select 
count(*) AS total_rows, 
count(distinct country) as countries,
count(distinct city) as cities,
count(distinct store_id) as stores,
count(distinct sku_id) as skus,
count(distinct category) as categories,
count(distinct subcategory) as subcategories,
count(distinct brand) as brands,
count(distinct channel)  as channels,
min(date) as first_date,
max(date) as last_date,
datediff(max(date), min(date)) as date_span_days
from raw_sales;
