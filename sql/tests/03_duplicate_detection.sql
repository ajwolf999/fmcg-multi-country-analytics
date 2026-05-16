-- Test: Duplicate detection
-- Expected: there could be duplicate sales from some stores
-- Result: PASS — zero duplicate store-SKU-date combinations found
-- Notes: zero duplicate combinations across 1.1M rows, natural key is clean


select count(*) as duplicate_combinations
from(
	select store_id,sku_id, date, count(*) as cnt
	from raw_sales 
	group by store_id, sku_id, date
	having count(*) >1) As duplicates
	
