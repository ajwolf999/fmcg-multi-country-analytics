INSERT INTO dim_date(date,year,month,day,weekofyear,weekday,is_weekend,is_holiday)
SELECT DISTINCT date, year, month, day, weekofyear,weekday, is_weekend,is_holiday
From raw_sales;

Insert INTO dim_store(store_id, country,city,channel,latitude,longitude)
SELECT DISTINCT store_id,country,city,channel,latitude,longitude
from raw_sales;

insert INTO dim_product(sku_id,sku_name,category,subcategory,brand,list_price)
SELECT DISTINCT sku_id,sku_name,category,subcategory,brand,list_price
from raw_sales;

INSERT INTO dim_supplier(supplier_id, purchase_cost, lead_time_days)
SELECT supplier_id, AVG(purchase_cost), ROUND(AVG(lead_time_days),0)
FROM raw_sales
group by supplier_id;

INSERT INTO fact_sales(date, store_id,sku_id,supplier_id,units_sold,discount_pct,promo_flag,gross_sales,net_sales,margin_pct,stock_on_hand,stock_out_flag,temperature,rain_mm)
SELECT date, store_id,sku_id,supplier_id,units_sold,discount_pct,promo_flag,gross_sales,net_sales,margin_pct,stock_on_hand,stock_out_flag,temperature,rain_mm
from raw_sales;