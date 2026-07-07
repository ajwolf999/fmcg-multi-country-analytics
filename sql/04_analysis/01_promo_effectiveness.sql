-- Analysis: Promotional Effectiveness by Category
-- Business question: Do promotions drive incremental volume and revenue,and at what cost to margin?
-- Method: Conditional aggregation comparing promo vs non-promo days across all 5 categories using promo_flag
-- Key finding: Promotions halve margin (0.40 → 0.21) across all categories.
--              Volume uplift ranges from 1.6x (Dairy) to 2.3x (Home Care).
--              Dairy generates higher net revenue WITHOUT promotions (435 vs 303).
--              Recommend reviewing Dairy promotional strategy.

select dp.category, count(*) as total_rows,
round(AVG(case when promo_flag = 1 then units_sold END),1) as Promo_days,
round(Avg(case when promo_flag =1 then net_sales END),2) as net_sales_promo,
round(Avg(case when promo_flag =1 then discount_pct END),2) as discount_pct_promo,
round(Avg(case when promo_flag =1 then margin_pct END),2) as margin_pct_promo,
round(Avg(case when promo_flag = 0 then units_sold END),1) as Non_promo_days,
round(Avg(case when promo_flag = 0 then net_sales END),2) as net_sales_no_promo,
round(Avg(case when promo_flag = 0 then discount_pct END),2) as discount_pct_no_promo,
round(Avg(case when promo_flag = 0 then margin_pct END),2) as margin_pct_no_promo
from fact_sales fs  
join dim_product dp ON fs.sku_id = dp.sku_id 
group by dp.category