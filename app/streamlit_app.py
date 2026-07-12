import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

st.set_page_config(page_title="FMCG Category Analytics", page_icon="📊", layout="wide")

@st.cache_resource
def get_engine():
    user = os.getenv("MYSQL_USER")
    pw   = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST", "mysql")
    port = os.getenv("MYSQL_PORT", "3306")
    db   = os.getenv("MYSQL_DATABASE")
    return create_engine(f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}",
    pool_pre_ping = True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10)

@st.cache_data(ttl=300)
def run_query(_engine, query):
    with _engine.connect() as conn:
        return pd.read_sql(text(query), conn)

st.title("📊 FMCG Multi-Country Category Analytics")
st.markdown("""
> **Portfolio project** — End-to-end business analysis of 1.1M FMCG sales transactions 
> across 7 European countries (2021-2023). Built with MySQL, Python, and Streamlit.
""")
st.divider()

# try:
#     engine = get_engine()
#     with engine.connect() as conn:
#         result = conn.execute(text("SELECT VERSION() AS version")).fetchone()
#     st.success(f"Connected to MySQL: {result.version}")
# except Exception as e:
#     st.error(f"Connection failed: {e}")
engine = get_engine()

# KPI queries
total_revenue = run_query(engine, 
    "SELECT ROUND(SUM(net_sales)/1000000, 2) AS value FROM fact_sales")

total_units = run_query(engine,
    "SELECT ROUND(SUM(units_sold)/1000000, 2) AS value FROM fact_sales")

stockout_loss = run_query(engine, """
    SELECT ROUND(
        SUM(avg_net * stockout_count)/1000000, 2
    ) AS value
    FROM (
        SELECT
            AVG(CASE WHEN stock_out_flag = 0 THEN net_sales END) as avg_net,
            SUM(CASE WHEN stock_out_flag = 1 THEN 1 ELSE 0 END) AS stockout_count
        FROM fact_sales
        GROUP BY store_id 
        ) sub
        """)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Revenue", f"€{total_revenue['value'][0]}M")
with col2:
    st.metric("Units Sold", f"{total_units['value'][0]}M")
with col3:
    st.metric("Countries", "7")
with col4:
    st.metric("Est. Stockout Loss", f"€{stockout_loss['value'][0]}M")

st.divider()

st.subheader("Net Revenue by Country")

country_sales = run_query(engine,"""
    SELECT ds.country,
        ROUND(SUM(fs.net_sales)/1000000, 2) AS net_revenue_m
    FROM fact_sales fs
    JOIN dim_store ds ON fs.store_id = ds.store_id
    GROUP BY ds.country
    ORDER BY net_revenue_m DESC
""")
fig = px.bar(
    country_sales,
    x="country",
    y="net_revenue_m",
    title="Net Revenue by country (€M)",
    labels={"net_revenue_m": "Net Revenue (€M)", "country": "Country"},
    color="net_revenue_m",
    color_continuous_scale="Blues"

)
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Units Sold by Category")
    category_units = run_query(engine,"""
        SELECT dp.category,
            ROUND(SUM(fs.units_sold)/1000000, 2) AS units_m
            FROM fact_sales fs
            JOIN dim_product dp ON fs.sku_id = dp.sku_id
            GROUP BY dp.category
            ORDER BY units_m DESC
    """)
    fig2 = px.pie(
        category_units,
        values="units_m",
        names="category",
        title="Units Sold by Category"
    )
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.subheader("Monthly Sales Trend (2022)")
    monthly = run_query(engine, """
        SELECT dd.month,
                ROUND(SUM(fs.net_sales)/1000000, 2) AS net_revenue_m
        FROM fact_sales fs
        JOIN dim_date dd ON fs.date = dd.date
        WHERE dd.year = 2022
        GROUP BY dd.month
        ORDER BY dd.month ASC
    """)
    fig3 = px.line(
        monthly,
        x="month",
        y="net_revenue_m",
        title="Monthly Net Revenue 2022 (€M)",
        labels={"net_revenue_m": "Net Revenue (€M)", "month": "Month"},
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)

st.divider()
st.caption("Data: Kaggle FMCG Multi-Country Sales Dataset | Built by Abhijit Sengupta")