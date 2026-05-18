-- Dim_date
CREATE TABLE IF NOT EXISTS dim_date (
    
    date            DATE         NOT NULL,
    year            SMALLINT     NOT NULL,
    month           TINYINT      NOT NULL,
    day             TINYINT      NOT NULL,
    weekofyear      TINYINT      NOT NULL,
    weekday         TINYINT      NOT NULL,
    is_weekend      TINYINT(1)   NOT NULL,
    is_holiday      TINYINT(1)   NOT NULL,

    
PRIMARY KEY (date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dim_store
CREATE TABLE IF NOT EXISTS dim_store (

    store_id        VARCHAR(20)  NOT NULL,
    country         VARCHAR(60)  NOT NULL,
    city            VARCHAR(80)  NOT NULL,
    channel         VARCHAR(40)  NOT NULL,
    latitude        DECIMAL(9,5),
    longitude       DECIMAL(9,5),

PRIMARY KEY (store_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dim_product
CREATE TABLE IF NOT EXISTS dim_product(

    sku_id          VARCHAR(20)  NOT NULL,
    sku_name        VARCHAR(120) NOT NULL,
    list_price      DECIMAL(10,2)  NOT NULL,
    category        VARCHAR(60)  NOT NULL,
    subcategory     VARCHAR(60)  NOT NULL,
    brand           VARCHAR(60)  NOT NULL,

PRIMARY KEY (sku_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dim_supplier
CREATE TABLE IF NOT EXISTS dim_supplier(

    supplier_id     VARCHAR(20) NOT NULL,
    purchase_cost   DECIMAL(10,2) NOT NULL,
    lead_time_days  TINYINT NOT NULL,
PRIMARY KEY (supplier_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Fact_sales
CREATE TABLE IF NOT EXISTS fact_sales(

date            DATE         NOT NULL,
store_id        VARCHAR(20)  NOT NULL,
sku_id          VARCHAR(20)  NOT NULL,
supplier_id     VARCHAR(20),
units_sold      INT          NOT NULL,
discount_pct    DECIMAL(5,4)  NOT NULL,
promo_flag      TINYINT(1)    NOT NULL,
gross_sales     DECIMAL(12,2) NOT NULL,
net_sales       DECIMAL(12,2) NOT NULL,
margin_pct      DECIMAL(6,4),
stock_on_hand   INT,
stock_out_flag  TINYINT(1),
temperature     DECIMAL(5,2),
    rain_mm         DECIMAL(6,2),
PRIMARY KEY (date, store_id, sku_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


