-- Test: Business logic checks — net sales formula, stockout consistency, promo discount logic
-- Expected: zero violations across all three checks
-- Result: PARTIAL PASS — net sales formula has 4,121 discrepancies, 30,580 stockout rows show units sold
-- Notes: 4,121 rows data has wrong sales and 30,580 has stockout but in the dataset it shows has sold units




select sum( case when round(net_sales,2) != Round(gross_sales*(1-discount_pct), 2) then 1 else 0 end) as invalid_net_sales_formula,
			sum( case when stock_out_flag =1 and units_sold > 0 then 1 else 0 end) as stockout_with_sales,
			sum( case when promo_flag =1 and discount_pct = 0 then 1 else 0 end) as promo_no_discount 
		from raw_sales rs 