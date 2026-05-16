-- Test: Distribution checks by country, channel, category
-- Expected: Relatively even distribution across dimensions
-- Result: PARTIAL — category distribution is balanced, but country and channel are skewed
-- Notes: Italy (32%) and Spain (24%) dominate country distribution. Hypermarket (48%) dominates channel. All row counts are exact multiples — confirms synthetic dataset.


-- Distribution by Country
select country, count(*) as row_count,
count(*) * 100.0 / 1100000 as pct_of_total
from raw_sales
group by country
order by row_count Desc;

-- Distribution by Channel
select channel, count(*) as row_count,
count(*) * 100.0 /1100000 as pct_of_total
from raw_sales 
group by channel 
order by row_count Desc;

-- Distribution by Category
select category, count(*) as row_count,
count(*) * 100.0 / 1100000 as pct_of_total
from raw_sales
group by category 
order by row_count desc;