import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# MySQL connection (local Docker)
MYSQL_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
    f"@localhost:3307/{os.getenv('MYSQL_DATABASE')}"
)

# SQLite output path — lives in app/ folder so Streamlit can access it
SQLITE_PATH = PROJECT_ROOT / "app" / "fmcg.db"
print(f"Project root: {PROJECT_ROOT}")
print(f"SQLite path: {SQLITE_PATH}")

TABLE_QUERIES = {
      "dim_date":     "SELECT * FROM dim_date",
    "dim_store":    "SELECT * FROM dim_store",
    "dim_product":  "SELECT * FROM dim_product",
    "dim_supplier": "SELECT * FROM dim_supplier",
    "fact_sales":   """
        SELECT date, store_id, sku_id, supplier_id,
               units_sold, gross_sales, net_sales,
               discount_pct, promo_flag, margin_pct,
               stock_out_flag
        FROM fact_sales
        where date < '2023-01-01'
    """

}

def main():
    print("Connecting to MySQL...")
    mysql_engine = create_engine(MYSQL_URL, pool_pre_ping = True)

    print(f"Creating SQLite database at {SQLITE_PATH}...")
    sqlite_conn = sqlite3.connect(SQLITE_PATH)


    for table, query in TABLE_QUERIES.items():
        print(f"Exporting {table}...")
        df = pd.read_sql(query, mysql_engine)
        df.to_sql(table, sqlite_conn, if_exists="replace", index=False)
        print(f"  → {len(df):,} rows exported")
    sqlite_conn.execute("vacuum")
    sqlite_conn.close()
    print(f"\n✓ SQLite database created: {SQLITE_PATH}")
    print(f"  Size: {SQLITE_PATH.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    main()