Data quality Report
Date = 13/05/2026
Dataset name: raw_sales
Prepared by : Abhijit Sengupta
Purpose : This document gives information about the dataset quality if business logic is matching, duplicate value, distribution checks and null analysis

Dataset Summary:
This dataset has 1.1M rows, 7 countries and 3 year date range
(13 stores, 9 cities across 7 countries and 5 categories)suggests synthetic/sample dataset. therefore, Analysis valid at store level, not representative of full country markets.

Completeness(null)
Zero nulls across all 18 columns checked. Synthetically clean dataset.

Uniqueness (duplicates)
Zero duplicate found store-sku-date.

Validity(range checks)
No negative units sold, discount price is less than 100%,gross sales is in positive number gross sales is more than net sales.

distribution checks
Italy (32%) and Spain (24%) dominate country distribution. Hypermarket (48%) dominates channel. Category is (relatively balanced at 16-24%).All row counts are exact multiples — confirms synthetic dataset.therefore cross-country comparisons should be normalized by row count to avoid bias in aggregated metrics

Business logic checks
net_sales = gross_sales \*(1-discount_pct)
4,121(0.37%) rows where net_sales doesn't match the formula. Therefore, net_sales should not be used as the sole revenue figure without validation.
30,580(2.8%) rows where stockout flag = 1 but units were still sold. Therefore, stockout impact analysis should treat these rows carefully - they may represent partial-day stockouts

Margin & Supplier Volatility
All 102 SKUs have exactly 60 distinct suppliers — impossible in real FMCG. Purchase costs vary by 1-4.4 currency units per SKU across the dataset. confirms synthetic data generation - suppliers ID's randomly assigned per transaction. therefore, supplier-level and cost-level analysis should not be used to draw real-world procurement conclusions.

Key findings and recommendations

This dataset has 7 countries and only 9 cities. so, it doesn't cover full country scope and the categories are limited to 5 and it has only 102 sku's, there are zero null value. Italy and Spain dominates the market. All 102 SKU's show 60 distinct suppliers each - therefore supplier performanace analysis is not meaningful in this dataset. Promotional, weather, and stockout analyses remain valid as they rely on sales figures not supplier data. this dataset is synthetic.

Limitation
This dataset is synthetic — generated programmatically rather than collected from real retail transactions. Evidence includes perfectly uniform row distribution across countries and channels, zero nulls across all 33 columns, and unrealistic purchase cost volatility for the same SKU across consecutive days. Findings should be interpreted as demonstrations of analytical methodology rather than real-world FMCG insights.
