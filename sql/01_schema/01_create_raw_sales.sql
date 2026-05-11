DROP TABLE IF EXISTS raw_sales;

CREATE TABLE  raw_sales (
    -- Date/time dimensions
      date            DATE         NOT NULL,
    year            SMALLINT     NOT NULL,
    month           TINYINT      NOT NULL,
    day             TINYINT      NOT NULL,
    weekofyear      TINYINT      NOT NULL,
    weekday         TINYINT      NOT NULL,
    is_weekend      TINYINT(1)   NOT NULL,
    is_holiday      TINYINT(1)   NOT NULL,

    -- Weather
    temperature     DECIMAL(5,2),
    rain_mm         DECIMAL(6,2),

    -- Store dimension
    store_id        VARCHAR(20)  NOT NULL,
    country         VARCHAR(60)  NOT NULL,
    city            VARCHAR(80)  NOT NULL,
    channel         VARCHAR(40)  NOT NULL,
    latitude        DECIMAL(9,5),
    longitude       DECIMAL(9,5),

    -- Product dimension
    sku_id          VARCHAR(20)  NOT NULL,
    sku_name        VARCHAR(120) NOT NULL,
    category        VARCHAR(60)  NOT NULL,
    subcategory     VARCHAR(60)  NOT NULL,
    brand           VARCHAR(60)  NOT NULL,

    -- Sales facts
    units_sold      INT          NOT NULL,
    list_price      DECIMAL(10,2) NOT NULL,
    discount_pct    DECIMAL(5,4)  NOT NULL,
    promo_flag      TINYINT(1)    NOT NULL,
    gross_sales     DECIMAL(12,2) NOT NULL,
    net_sales       DECIMAL(12,2) NOT NULL,

    -- Supply chain
    stock_on_hand   INT,
    stock_out_flag  TINYINT(1),
    lead_time_days  TINYINT,
    supplier_id     VARCHAR(20),
    purchase_cost   DECIMAL(10,2),
    margin_pct      DECIMAL(6,4),

    -- Indexes for the queries we'll run later
    KEY idx_date (date),
    KEY idx_country (country),
    KEY idx_category (category),
    KEY idx_store_sku_date (store_id, sku_id, date),
    KEY idx_promo (promo_flag, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

