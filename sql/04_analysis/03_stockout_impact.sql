-- Analysis: Stockout Impact by Country
-- Business question: How much revenue is lost to stockouts, and which markets are most affected?
-- Method: Baseline average net_sales from non-stockout rows multiplied by stockout row count, grouped by country
-- Key finding: Stockouts affect approximately 3% of all transactions consistently across every market, representing an estimated €14.6M in lost revenue over the 3-year period. Italy alone accounts for €4.2M of this due to its larger transaction volume. While the stockout rate itself is uniform across countries, the absolute revenue impact scales with market size — suggesting inventory management improvements would yield the largest absolute returns in Italy and Spain, the two largest markets.

select ds.country, count(*) as total_rows,
round(avg(case when stock_out_flag = 0 Then net_sales END) * sum(case when stock_out_flag = 1 then 1 else 0 END),2)  as Estimated_lost_revenue,
sum(case when stock_out_flag =1 then 1 else 0 end)  as stockout_rows,
round(sum(case when stock_out_flag = 1 then 1 else 0 end) / count(*) *100, 2) as stockout_rate_pct
from fact_sales fs
join dim_store ds on fs.store_id = ds.store_id
group by ds.country