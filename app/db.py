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

def is_cloud() -> bool:
    """ Return True if running in Streamlit Community Cloud."""
    return os.getenv("STREAMLIT_SHARING_MODE") is not None

@st.cache_resource
def get_engine():
    if is_cloud():
        # SQLite for cloud deployment
        db_path = Path(__file__).parent / "fmcg.db"
        return create_engine(f"sqlite:///{db_path}")
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
