"""
Database connection handler.
Automatically detects environment:
- Streamkit Cloud  → SQLite (fmcg.db bundled with app)
- Local Docker    → MySQL (via environment variables)
"""

import os 
from pathlib import Path
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


@st.cache_resource
def get_engine():
   """
   Use SQLite if fmcg.db exists alongside this file.
    Otherwise fall back to MySQL via environment variables.
   """
   sqlite_path = Path(__file__).parent / "fmcg.db"

   
   if sqlite_path.exists():
        return create_engine(f"sqlite:///{sqlite_path}")
   else:
        # MySQL for local Docker Development
        user = os.getenv("MYSQL_USER")
        pw = os.getenv("MYSQL_PASSWORD")
        host = os.getenv("MYSQL_HOST", "mysql")
        port = os.getenv("MYSQL_PORT","3306")
        db = os.getenv("MYSQL_DATABASE")
        return create_engine(
            f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}",
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10
        )

@st.cache_data(ttl=300)
def run_query(_engine,query):
    with _engine.connect() as conn:
        return pd.read_sql(text(query),conn)

