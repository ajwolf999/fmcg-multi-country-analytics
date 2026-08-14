import os 
import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine, text

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
def run_query(_engine, query):
    with _engine.connect() as conn:
        return pd.read_sql(text(query), conn)

st.set_page_config(
    page_title="Data Quality",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Data Quality Report")
st.markdown("""
This page summarises the data quality findings from profiling 1.1M rows 
of FMCG sales data across 7 European countries (2021-2023).
""")
st.divider()

engine = get_engine()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Rows", "1,100,000")
with col2:
    st.metric("Countries", "7")
with col3:
    st.metric("Stores", "13")
with col4:
    st.metric("SKUs","102")
with col5:
    st.metric("Date Range", "2021-2023")
st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Row Distribution by Country")
    country_dist = run_query(engine,"""
        SELECT ds.country,
                COUNT(*) AS row_count,
                ROUND(COUNT(*)* 100.0 / 1100000, 1) AS pct
        FROM fact_sales fs
        JOIN dim_store ds on fs.store_id = ds.store_id
        GROUP BY ds.country
        ORDER BY row_count DESC                
    """)
    fig1 = px.bar(
        country_dist,
        x="country",
        y="pct",
        title="% of Total Rows by Country",
        labels={"pct": "% of Total","country": "Country"},
        color="pct",
        color_continuous_scale="Blues"
    )
   
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Row Distribution by Category")
    category_dist = run_query(engine, """
        SELECT dp.category,
            COUNT(*) as row_count,
            ROUND(COUNT(*)* 100.0 / 1100000, 1) AS pct
        FROM fact_sales fs
        JOIN dim_product dp ON fs.sku_id = dp.sku_id
        GROUP BY dp.category
        ORDER BY row_count DESC

    """)
    fig2 = px.pie(
        category_dist,
        values='pct',
        names="category",
        title="% of Total Rows by Category"
    )
    st.plotly_chart(fig2, use_container_width=True)
st.divider()

st.subheader("Data Quality Test Results")

quality_checks = {
    "Test": [
        "Null values (18 columns)",
        "Duplicate store-SKU-date combinations",
        "Negative units sold",
        "Discount > 100%",
        "Negative gross sales",
        "Net sales > gross sales",
        "Net sales formula mismatch",
        "Stockout rows with units sold",
        "Promo rows with zero discount",
        "Referential integrity — dim_date",
        "Referential integrity — dim_store",
        "Referential integrity — dim_product",
        "Referential integrity — dim_supplier"
    ],
    "Result": [
        "PASS", "PASS", "PASS", "PASS", "PASS",
        "PASS", "FAIL", "FAIL", "PASS",
        "PASS", "PASS", "PASS", "PASS"
    ],
    "Finding": [
        "0 nulls across all columns",
        "0 duplicates found",
        "0 rows",
        "0 rows",
        "0 rows",
        "0 rows",
        "4,121 rows (0.37%)",
        "30,580 rows (2.8%)",
        "0 rows",
        "0 orphaned rows",
        "0 orphaned rows",
        "0 orphaned rows",
        "0 orphaned rows"
    ]
}

import pandas as pd
df_quality = pd.DataFrame(quality_checks)

def highlight_result(val):
    color = "#c8e6c9" if val == "PASS" else "#ffcdd2"
    return f"background-color: {color}"

st.dataframe(
    df_quality.style.applymap(highlight_result, subset=["Result"]),
    use_container_width=True,
    hide_index=True
)

st.divider()

st.subheader("Key Limitations")
st.warning("""
**Synthetic Dataset:** This dataset was generated programmatically, not collected 
from real retail transactions. Evidence: perfectly uniform row distribution, 
zero nulls across all columns, 60 suppliers per SKU (impossible in real FMCG), 
and unrealistic purchase cost volatility. Findings demonstrate analytical 
methodology rather than real-world FMCG insights.
""")

st.caption("Data: Kaggle FMCG Multi-Country Sales Dataset | Built by Abhijit Sengupta")