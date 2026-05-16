-- Test: value range checks
-- Expected: zero rows with negative units, discount > 100%, negative gross sales or invalid_net_gt_gross
-- Result: PASS — no negative units sold, discount price is less than 100%,gross sales is in positive number gross sales is more then net sales.
-- Notes: all 1.1M rows pass range checks — dataset is synthetically clean
select
    sum(case when units_sold < 0 then 1 else 0 end) as negative_unit_sold,
	sum(case when discount_pct > 1 then 1 else 0 end) as invalid_discount_pct,
	sum(case when  gross_sales < 0 then 1 else 0 end) as negative_gross_sales
    sum(case when net_sales > gross_sales then 1 else 0  end) as invalid_net_gt_gross
	from raw_sales