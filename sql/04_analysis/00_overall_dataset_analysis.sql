
-- Total gross sales, net sales, difference in sales and difference percentage by country (Join)
select country,
round(sum(gross_sales),2) as total_gross_sales,
round(sum(net_sales),2) as total_net_sales,
sum(gross_sales)-sum(net_sales) as difference_sales,
round((sum(gross_sales)-sum(net_sales))/sum(gross_sales)*100,2) as overall_discount_pct_sales
from fact_sales fs
join dim_store ds ON fs.store_id = ds.store_id
group by ds.country
order by total_gross_sales desc

-- Top 10 best-selling SKU's (Join)
select dp.sku_id,dp.sku_name,sum(fs.units_sold ) as total_unit_sold
from fact_sales fs 
join dim_product dp ON fs.sku_id = dp.sku_id 
group by dp.sku_id, dp.sku_name 
order by total_unit_sold desc
limit 10

-- Promotional transaction rate per channel (JOIN)
select ds.channel, count(*) as total_rows,
sum(case when promo_flag = 1 then 1 ELSE 0 END) as promo_rows,
round(sum(case when promo_flag = 1 then 1 ELSE 0 END)/ count(*)*100,1) as promotional_transaction_PCT
from dim_store ds 
JOIN fact_sales fs on ds.store_id = fs.store_id 
group by ds.channel 


--Highest average daily sales by month (JOIN)

-- Sales peak in summer months (June-August) driven by seasonal demand for Beverages and Snacks — categories that correlate with outdoor activity and warmer temperatures. December shows a secondary peak driven by festive consumption across all categories, particularly Dairy and Snacks. March is the weakest month, consistent with post-winter, pre-summer low demand. This seasonality pattern suggests inventory planning should weight summer and December periods 12-14% higher than the March trough.
select dd.`month`,sum(fs.net_sales ) as total_sales
from fact_sales fs 
join dim_date dd on fs.`date` = dd.`date` 
where year = 2022
group by `month` 
order by `month` asc

-- Stockout rate and estimated revenue lost per country.

-- Stockouts affect approximately 3% of all transactions consistently across every market, representing an estimated €14.6M in lost revenue over the 3-year period. Italy alone accounts for €4.2M of this due to its larger transaction volume. While the stockout rate itself is uniform across countries, the absolute revenue impact scales with market size — suggesting inventory management improvements would yield the largest absolute returns in Italy and Spain, the two largest markets.

select ds.country, count(*) as total_rows,
avg(case when stock_out_flag = 0 Then net_sales END) * sum(case when stock_out_flag = 1 then 1 else 0 END)  as Estimated_lost_revenue,
sum(case when stock_out_flag =1 then 1 else 0 end)  as stockout_rows,
round(sum(case when stock_out_flag = 1 then 1 else 0 end) / count(*) *100, 2) as stockout_rate_pct
from fact_sales fs
join dim_store ds on fs.store_id = ds.store_id
group by ds.country

-- Show total units sold and total net sales per category and channel combination.

-- "Hypermarket dominates every category as it is the largest category by (48% of transactions). Bevrages and Snacks lead in Hypermarket with ~9.5-9.8M units each.Convenience is tiny across all categories — consistent with its 4.4% and Home Care barely registers at 138K units in Convenience.Snacks generates more net sales than Beverages in Hypermarket (73.7M vs 57.2M) despite Beverages having higher unit volume (9.8M vs 9.3M). That means Snacks has a higher average price per unit than Beverages".
select category, channel, sum(units_sold)as total_units_sold, sum(net_sales) as total_net_sales
from fact_sales fs 
Join dim_product dp on fs.sku_id = dp.sku_id
join dim_store ds on fs.store_id = ds.store_id 
group by category, channel 
order by total_units_sold desc



-- Germany only has 2 stores total(out of 13 stores across the whole dataset), both are conecentrated in berlin. there's no second city represented.
select ds.store_id, city,sum(fs.units_sold ) as total_units
from fact_sales fs 
Join dim_store ds on fs.store_id = ds.store_id 
where country = 'Germany'
group by ds.store_id, city 
having sum(fs.units_sold )> 50000
order by total_units  desc

-- 2022 shows a clear bimodal seasonal pattern — a primary summer peak in July (€14.2M) driven by Beverage and Snack demand, and a secondary festive peak in December (€14.1M). February is the weakest month at €11.8M — 16% below the July peak. The trough between peaks runs from September to October before recovering into the year-end festive period.

select dd.`month`,sum(fs.net_sales ) as total_sales
from fact_sales fs 
join dim_date dd on fs.`date` = dd.`date` 
where year = 2022
group by `month` 
order by `month` asc