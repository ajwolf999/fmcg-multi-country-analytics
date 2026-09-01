# Data Dictionary

## dim_date

| Column     | Type       | Description                  |
| ---------- | ---------- | ---------------------------- |
| date       | DATE (PK)  | Calendar date, primary key   |
| year       | SMALLINT   | Calendar year                |
| month      | TINYINT    | Calendar month (1–12)        |
| day        | TINYINT    | Day of month                 |
| weekofyear | TINYINT    | ISO week number              |
| weekday    | TINYINT    | Day of week (0=Monday)       |
| is_weekend | TINYINT(1) | 1 if Saturday/Sunday, else 0 |
| is_holiday | TINYINT(1) | 1 if public holiday, else 0  |

## dim_store

| Column    | Type             | Description                                                             |
| --------- | ---------------- | ----------------------------------------------------------------------- |
| store_id  | VARCHAR(20) (PK) | Unique store identifier                                                 |
| country   | VARCHAR(60)      | Country where store is located                                          |
| city      | VARCHAR(80)      | City where store is located                                             |
| channel   | VARCHAR(40)      | Retail channel (e.g. Hypermarket, Supermarket, E-commerce, Convenience) |
| latitude  | DECIMAL(9,5)     | Store geographic latitude                                               |
| longitude | DECIMAL(9,5)     | Store geographic longitude                                              |

## dim_product

| Column      | Type             | Description                                         |
| ----------- | ---------------- | --------------------------------------------------- |
| sku_id      | VARCHAR(20) (PK) | Unique product (SKU) identifier                     |
| sku_name    | VARCHAR(120)     | Product name                                        |
| category    | VARCHAR(60)      | Top-level product category (e.g. Beverages, Snacks) |
| subcategory | VARCHAR(60)      | Product subcategory                                 |
| brand       | VARCHAR(60)      | Product brand                                       |
| list_price  | DECIMAL(10,2)    | Standard (pre-discount) unit price                  |

## dim_supplier

| Column         | Type             | Description                                                 |
| -------------- | ---------------- | ----------------------------------------------------------- |
| supplier_id    | VARCHAR(20) (PK) | Unique supplier identifier                                  |
| purchase_cost  | DECIMAL(10,2)    | Average purchase cost across transactions for this supplier |
| lead_time_days | TINYINT          | Average delivery lead time in days                          |

## fact_sales

| Column         | Type                               | Description                                              |
| -------------- | ---------------------------------- | -------------------------------------------------------- |
| date           | DATE (PK, FK → dim_date)           | Transaction date                                         |
| store_id       | VARCHAR(20) (PK, FK → dim_store)   | Store where sale occurred                                |
| sku_id         | VARCHAR(20) (PK, FK → dim_product) | Product sold                                             |
| supplier_id    | VARCHAR(20) (FK → dim_supplier)    | Supplier for this transaction                            |
| units_sold     | INT                                | Number of units sold                                     |
| discount_pct   | DECIMAL(5,4)                       | Discount applied (0–1 scale)                             |
| promo_flag     | TINYINT(1)                         | 1 if transaction occurred during a promotion, else 0     |
| gross_sales    | DECIMAL(12,2)                      | Revenue before discount                                  |
| net_sales      | DECIMAL(12,2)                      | Revenue after discount                                   |
| margin_pct     | DECIMAL(6,4)                       | Profit margin (0–1 scale)                                |
| stock_on_hand  | INT                                | Inventory level at time of transaction                   |
| stock_out_flag | TINYINT(1)                         | 1 if store was out of stock, else 0                      |
| temperature    | DECIMAL(5,2)                       | Recorded temperature (°C) at store location on this date |
| rain_mm        | DECIMAL(6,2)                       | Recorded rainfall (mm) at store location on this date    |

**Note:** `fact_sales` uses a composite primary key of `(date, store_id, sku_id)`, verified unique via referential integrity testing (see `sql/tests/03_duplicate_detection.sql`).
