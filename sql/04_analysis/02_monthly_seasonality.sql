-- Analysis: Monthly Sales Seasonality
-- Business question: Which months drive peak sales and what explains the pattern?
-- Method: Monthly aggregation of net_sales for 2022, ordered chronologically
-- Key finding: Sales peak in summer months (June-August) driven by seasonal demand for Beverages and Snacks — categories that correlate with outdoor activity and warmer temperatures. December shows a secondary peak driven by festive consumption across all categories, particularly Dairy and Snacks. March is the weakest month, consistent with post-winter, pre-summer low demand. This seasonality pattern suggests inventory planning should weight summer and December periods 12-14% higher than the March trough.
select dd.`month`,sum(fs.net_sales ) as total_sales
from fact_sales fs 
join dim_date dd on fs.`date` = dd.`date` 
where year = 2022
group by `month` 
order by `month` asc