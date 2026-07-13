import os
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text


st.set_page_config(
    page_title="Deep Dive Analysis",
    page_icon="🔍",
    layout="wide"
)

@st.cache_resource
def get_engine():
    user = os.getenv("MYSQL_USER")
    pw   = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST", "mysql")
    port = os.getenv("MYSQL_PORT", "3306")
    db   = os.getenv("MYSQL_DATABASE")
    return create_engine(
        f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}",
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10
    )

@st.cache_data(ttl=300)
def run_query(_engine, query, params=None):
    with _engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)
    
engine = get_engine()


st.title("🔍 Country & Category Deep Dive")
st.markdown("Filter by country and category to explore sales performance.")
st.divider()

# Load filter options from database
countries = run_query(engine,
    "SELECT DISTINCT country from dim_store ORDER BY country")
categories = run_query(engine,
    "SELECT DISTINCT category FROM dim_product ORDER by category")

# Sidebar filters
st.sidebar.header("Filters")
selected_country = st.sidebar.selectbox(
    "Select Country",
    options=["All"] + countries["country"].tolist()

)
selected_category = st.sidebar.selectbox(
    "Select Category",
    options=["All"]+ categories["category"].tolist()
)

# Build WHERE clause based on selections
where_conditions = []
if selected_country != "All":
    where_conditions.append(f"ds.country = '{selected_country}'")
if selected_category != "All":
    where_conditions.append(f"dp.category = '{selected_category}'")

where_clause = "WHERE " + " AND ".join(where_conditions) if where_conditions else ""

st.subheader(f"Monthly Revenue Trend - {selected_country} | {selected_category}")

monthly_query = f"""
    SELECT dd.year, dd.month,
        ROUND(SUM(fs.net_sales)/1000,2) AS net_revenue_k
        FROM fact_sales fs
        JOIN dim_store ds ON fs.store_id = ds.store_id
        JOIN dim_product dp ON fs.sku_id = dp.sku_id
        JOIN dim_date dd ON fs.date = dd.date
        {where_clause}
        GROUP BY dd.year, dd.month
        ORDER BY dd.year, dd.month
"""
monthly_data = run_query(engine, monthly_query)
monthly_data["period"] = monthly_data["year"].astype(str) + "-" + monthly_data["month"].astype(str).str.zfill(2)

fig1 = px.line(
    monthly_data,
    x="period",
    y="net_revenue_k",
    title="Monthly Net Revenue (€K)",
    labels={"net_revenue_k": "Net Revenue (€K)", "period": "Month"},
    markers=True
)
fig1.update_xaxes(tickangle=45)
st.plotly_chart(fig1, use_container_width=True)


col_left, col_right = st.columns(2)

with col_left:
    st.subheader(" Top 10 Sku's by Units Sold")

    top_skus_query = f"""
        SELECT dp.sku_name,
                SUM(fs.units_sold) AS total_units
        FROM fact_sales fs
        JOIN dim_store ds ON fs.store_id = ds.store_id
        JOIN dim_product dp ON fs.sku_id = dp.sku_id
        {where_clause}
        GROUP BY dp.sku_name
        ORDER BY total_units DESC
        LIMIT 10
    """

    top_skus = run_query(engine, top_skus_query)

    fig2 = px.bar(
        top_skus,
        x="total_units",
        y="sku_name",
        orientation="h",
        title="Top 10 SKUs",
        labels={"total_units": "Units Sold", "sku_name": "SKU"}
    
    )
    fig2.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.subheader("Promo vs Non-Promo Performance")

    promo_query = f"""
        SELECT
            CASE WHEN fs.promo_flag = 1 THEN 'Promo' ELSE 'Non-Promo' END as promo_type,
            ROUND(AVG(fs.units_sold), 1) AS avg_units,
            ROUND(AVG(fs.net_sales), 2) AS avg_net_sales,
            ROUND(AVG(fs.margin_pct), 3) AS avg_margin
            FROM fact_sales fs
            JOIN dim_store ds ON fs.store_id = ds.store_id
            JOIN dim_product dp ON fs.sku_id = dp.sku_id
            {where_clause}
            GROUP  BY fs.promo_flag
         """
    promo_data = run_query(engine, promo_query)
    
    fig3 = px.bar(
        promo_data,
        x="promo_type",
        y="avg_units",
        title="Avg Units Sold: Promo vs Non-Promo",
        labels={"avg_units": "Avg Units Sold", "promo_type": ""},
        color="promo_type",
        color_discrete_map={"Promo": "#2196F3", "Non-Promo": "#90CAF9"}
    )
    st.plotly_chart(fig3, use_container_width=True)
    
    st.dataframe(promo_data, use_container_width=True, hide_index=True)

st.divider()
st.caption("Data: Kaggle FMCG Multi-Country Sales Dataset | Built by Abhijit Sengupta")
        
    