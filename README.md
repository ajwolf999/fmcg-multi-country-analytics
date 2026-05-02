# FMCG Multi-Country Category Analytics

> Portfolio project demonstrating end-to-end analytics work on FMCG sales data — from MySQL data modeling through Dockerized deployment.

**Status:** 🚧 Work in progress

## What this project does

Analyzes a multi-country FMCG sales dataset to surface category performance issues, data quality gaps, and revenue opportunities — the kind of analysis a Business Analyst at NielsenIQ or a similar firm would deliver to an FMCG client.

## Tech stack

- **Database:** MySQL 8.4 (Docker)
- **ETL:** Python (Pandas, SQLAlchemy)
- **Modeling:** Layered SQL (raw → staging → marts)
- **App:** Streamlit + Plotly
- **Container:** Docker Compose
- **Source data:** [Kaggle FMCG Multi-Country Sales Dataset](https://www.kaggle.com/datasets)

## How to run

```bash
git clone <this repo>
cd fmcg_project
cp .env.example .env  # then edit .env with your own passwords
docker-compose up -d
# Streamlit app: http://localhost:8501
# MySQL via DBeaver: localhost:3307
```

## Repository structure

- `data/raw/` — source CSV (gitignored, download from Kaggle)
- `ingestion/` — Python ETL scripts (CSV → MySQL)
- `sql/01_schema/` — table definitions
- `sql/02_staging/` — cleaning views
- `sql/03_marts/` — fact and dimension tables
- `sql/04_analysis/` — business questions answered as SQL
- `sql/tests/` — data quality checks
- `app/` — Streamlit dashboard
- `docs/` — BRD, insights memo, data dictionary

## Author

Abhijit Sengupta — Business Analyst, ex-NielsenIQ
[LinkedIn](https://www.linkedin.com/in/aedwulf/) · Warsaw, Poland
