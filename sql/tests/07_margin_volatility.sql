-- Test: Purchase cost volatility and supplier count per SKU
-- Expected: Stable costs with 1-3 suppliers per SKU (real FMCG pattern)
-- Result: FAIL all 102 SKU's have exactly 60 suppliers, cost ranges of 1-4.4 units
-- Notes: In real scenerio there would be 1-3 suppliers for a product. 

select sku_id, min(purchase_cost) as lowest_cost_recorderd,
max(purchase_cost) as highest_cost_recorded,
MAX(purchase_cost) - min(purchase_cost) as cost_range,
count(distinct supplier_id) as supplier_count
from raw_sales rs 
group by sku_id 
HAVING   cost_range >1
order by cost_range desc