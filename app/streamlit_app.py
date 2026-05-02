import os
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="FMCG Category Analytics", layout="wide")

@st.cache_resource
def get_engine():
    user = os.getenv("MYSQL_USER")
    pw   = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST", "mysql")
    port = os.getenv("MYSQL_PORT", "3306")
    db   = os.getenv("MYSQL_DATABASE")
    return create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}")

st.title("FMCG Multi-Country Category Analytics")
st.caption("Portfolio project — Day 1 sanity check")

try:
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION() AS version")).fetchone()
    st.success(f"Connected to MySQL: {result.version}")
except Exception as e:
    st.error(f"Connection failed: {e}")