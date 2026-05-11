import os # reads env vars (DB credentials)
import time     # tracks how long the load takes
from pathlib import Path   # handles file paths cleanly across Mac/Windows/Linux

import pandas as pd    # reads CSV, writes to MySQL
from dotenv import load_dotenv    # loads .env file into os.environ
from sqlalchemy import create_engine, text  # database connection + raw SQL execution


# Configuration — all paths and settings in one place



PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT/".env")

CSV_PATH = PROJECT_ROOT/"data"/"raw"/"fmcg_sales.csv"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "01_schema" / "01_create_raw_sales.sql"
TABLE_NAME  = "raw_sales"
CHUNK_SIZE  = 50_000   # rows per chunk — balances memory vs speed

DB_USER = os.getenv("MYSQL_USER")
DB_PASS = os.getenv("MYSQL_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE")
DB_HOST = "localhost"
DB_PORT = 3307





def get_engine():
    url = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    return create_engine(url, pool_pre_ping=True)

# def create_schema(engine):
#     print(f"Reading schema from{SCHEMA_PATH.name}...")
#     ddl = SCHEMA_PATH.read_text()

#     statements = [s.strip() for s in ddl.split(";") if s.strip()]

#     with engine.begin() as conn:
#         for stmt in statements:
#             conn.execute(text(stmt))
#     print("✓ Schema created.")
def create_schema(engine):
    print(f"Reading schema from {SCHEMA_PATH.name}...")
    ddl = SCHEMA_PATH.read_text()
    # Splits on semicolons, skip anything that's only comments or whitespace
    statements = []
    for stmt in ddl.split(";"):
        #Remove commit lines and whitespace
        lines = [
            line for line in stmt.splitlines()
            if line.strip() and not line.strip().startswith("--")
        ]
        if lines: #only add if there's actual SQL content
            statements.append(stmt.strip())
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))
    print("✓ Schema created.")



def load_csv(engine):
    """
    Stream the CSV in 50k-row chunks and append to MySQL.
    Memory stays flat — we never load the full 212MB at once.
    """
    print(f"\nLoading {CSV_PATH.name} → {TABLE_NAME}")
    print(f"Chunk size: {CHUNK_SIZE:,} rows | "
        f"Expected chunks: ~'{1_100_000//CHUNK_SIZE+1}")

    start = time.time()
    total_rows = 0
    # read_csv with chunksize returns an iterator, NOT a DataFrame.
    # Each iteration gives you the next 50k rows as a DataFrame.

    reader = pd.read_csv(
        CSV_PATH,
        chunksize=CHUNK_SIZE,
        parse_dates=["date"], # convert the date column to Python datetime

    )

    for i, chunk in enumerate(reader, start=1):
        chunk.to_sql(
            TABLE_NAME,
            engine,
            if_exists="append", # append to existing table (we created it above)
            index=False,  # don't write the DataFrame's row index as a column
            method="multi", # batch multiple rows per INSERT statement (faster)
            chunksize=5_000, # SQLAlchemy sub-batch size within each Pandas chunk
        )

        total_rows += len(chunk)
        elapsed = time.time() - start
        rate = total_rows / elapsed if elapsed > 0 else 0

        print(f"  Chunk {i:>3} | "
            f"{total_rows:>10,} rows | "
            f"{elapsed:>6.1f}s | "
              f"~{rate:>7,.0f} rows/sec"
        )

    print(f"\n✓ Loaded {total_rows:,} rows in {time.time() - start:.1f}s")

def verify(engine):
    """
    Sanity-check the load with aggregate queries.
    These become the first entries in your data quality report.
    """
    print("\nVerifying load...")

    checks = {
        "Total rows":           f"SELECT COUNT(*) FROM {TABLE_NAME}",
        "Distinct countries":   f"SELECT COUNT(DISTINCT country) FROM {TABLE_NAME}",
        "Distinct stores":      f"SELECT COUNT(DISTINCT store_id) FROM {TABLE_NAME}",
        "Distinct SKUs":        f"SELECT COUNT(DISTINCT sku_id) FROM {TABLE_NAME}",
        "Distinct categories":  f"SELECT COUNT(DISTINCT category) FROM {TABLE_NAME}",
        "Date range":           f"SELECT MIN(date), MAX(date) FROM {TABLE_NAME}",
        "Null check (net_sales)": f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE net_sales IS NULL",
        "Stockout rows":        f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE stock_out_flag = 1",
    }

    with engine.connect() as conn:
        for label, query in checks.items():
            result = conn.execute(text(query)).fetchone()
            # fetchone() returns a tuple — unpack nicely
            value = result[0] if len(result) == 1 else f"{result[0]} → {result[1]}"
            print(f"  {label:<30} {value}")

def verify(engine):
    """
    Sanity-check the load with aggregate queries.
    These become the first entries in your data quality report.
    """
    print("\nVerifying load...")

    checks = {
        "Total rows":           f"SELECT COUNT(*) FROM {TABLE_NAME}",
        "Distinct countries":   f"SELECT COUNT(DISTINCT country) FROM {TABLE_NAME}",
        "Distinct stores":      f"SELECT COUNT(DISTINCT store_id) FROM {TABLE_NAME}",
        "Distinct SKUs":        f"SELECT COUNT(DISTINCT sku_id) FROM {TABLE_NAME}",
        "Distinct categories":  f"SELECT COUNT(DISTINCT category) FROM {TABLE_NAME}",
        "Date range":           f"SELECT MIN(date), MAX(date) FROM {TABLE_NAME}",
        "Null check (net_sales)": f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE net_sales IS NULL",
        "Stockout rows":        f"SELECT COUNT(*) FROM {TABLE_NAME} WHERE stock_out_flag = 1",
    }

    with engine.connect() as conn:
        for label, query in checks.items():
            result = conn.execute(text(query)).fetchone()
            # fetchone() returns a tuple — unpack nicely
            value = result[0] if len(result) == 1 else f"{result[0]} → {result[1]}"
            print(f"  {label:<30} {value}")

def main():
    print("=" * 55)
    print("FMCG Sales ETL — CSV to MySQL")
    print("=" * 55)

    engine = get_engine()
    create_schema(engine)
    load_csv(engine)
    verify(engine)

    print("\n" + "=" * 55)
    print("✓ ETL complete. Data ready for analysis.")
    print("=" * 55)


if __name__ == "__main__":
    main()