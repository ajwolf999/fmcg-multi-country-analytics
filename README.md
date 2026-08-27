# FMCG Multi-Country Category Analytics

> End-to-end analytics pipeline analyzing 1.1M FMCG sales transactions across 7 European countries — from raw data ingestion through star schema modeling to a live interactive dashboard. Quantifies promotional effectiveness, seasonal patterns, and stockout revenue impact to inform category management decisions.

🔗 **[Live Dashboard](https://fmcg-multi-country-analytics-europe.streamlit.app/)** &nbsp;|&nbsp; 💻 **[GitHub Repo](https://github.com/ajwolf999/fmcg-multi-country-analytics)**

---

## The Business Problem

A category manager at an FMCG company needs to answer three recurring questions:

1. **Are our promotions actually profitable**, or are we giving away margin for volume that doesn't compensate?
2. **When should we adjust inventory** for seasonal demand shifts?
3. **How much revenue are we losing to stockouts**, and where should we prioritize fixes?

This project answers all three using a multi-country FMCG dataset (1.1M transactions, 2021-2023, 7 European countries), applying the same analytical rigor used for enterprise client data during 4 years as a Business Analyst at NielsenIQ.

---

## Key Findings

| Question                    | Finding                                                                                                                                                                                   |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Do promotions work?**     | Promotions cut margin nearly in half (40% → 21%) across all categories, while driving only 1.6x–2.3x volume uplift. Dairy generates _more_ net revenue without promotions than with them. |
| **When does demand peak?**  | Sales peak in July (summer) and December (festive), 20% above the February trough — driven by Beverages and Snacks.                                                                       |
| **What do stockouts cost?** | An estimated **€14.6M in lost revenue** (2021–2023), with Italy and Spain — the two largest markets — accounting for 52% of total impact.                                                 |

---

## Tech Stack

| Layer           | Tools                                            |
| --------------- | ------------------------------------------------ |
| Database        | MySQL 8.4 (Docker)                               |
| ETL             | Python, Pandas, SQLAlchemy                       |
| Data Modeling   | Star schema (raw → staging → marts), layered SQL |
| Dashboard       | Streamlit, Plotly                                |
| Deployment      | Streamlit Community Cloud (SQLite)               |
| Version Control | Git, GitHub                                      |
| Local Dev       | Docker Compose, DBeaver, VS Code                 |

---

## Architecture

---

## Data Engineering Highlights

- **1.1M rows** loaded via a chunked Python ETL pipeline — memory-safe streaming rather than a single bulk load
- **Star schema** with 4 dimension tables and 1 fact table, composite primary keys, and 5 targeted indexes based on known query patterns
- **8-test data quality framework** covering nulls, duplicates, value ranges, business logic, and referential integrity — full results in [`docs/data_quality_report.md`](docs/data_quality_report.md)
- **Zero referential integrity violations** across 1.1M fact rows against all 4 dimensions
- **Deployment engineering**: exported and compressed a cloud-ready SQLite database (212MB → 52MB) with environment-aware connection logic so the same codebase runs on local Docker/MySQL and Streamlit Cloud/SQLite

---

## Dashboard Preview

**Page 1 — Executive Summary:** KPI cards (revenue, units, stockout loss) + country/category/seasonality charts
**Page 2 — Deep Dive:** Interactive filters by country and category with dynamic revenue trends and top-SKU analysis
**Page 3 — Data Quality:** Dataset profile, distribution charts, and full test-suite results

---

## How to Run Locally

```bash
git clone https://github.com/ajwolf999/fmcg-multi-country-analytics.git
cd fmcg-multi-country-analytics

# Set up environment variables
cp .env.example .env
# Edit .env with your own MySQL credentials

# Start MySQL + Streamlit
docker-compose up -d

# App:    http://localhost:8501
# MySQL:  localhost:3307 (via DBeaver or similar)
```

**Note:** The Kaggle source CSV is not included (gitignored). Download the [FMCG Multi-Country Sales Dataset](https://www.kaggle.com/datasets) and place it in `data/raw/` to reproduce the ETL from scratch, or use the pre-built `app/fmcg.db` SQLite file for a quick look at the dashboard.

---

## Repository Structure

---

## About Me

**Abhijit Sengupta** — Business Analyst, ex-NielsenIQ (4 years, FMCG & retail analytics across 15+ enterprise clients)

Pivoting toward broader Business/Data Analyst roles across industries. This project demonstrates the full analytical lifecycle — data engineering, quality assurance, business analysis, and stakeholder-ready reporting — that I applied professionally at NielsenIQ, rebuilt end-to-end on a public dataset.

📍 Warsaw, Poland · Open to remote (EU) · Available immediately
🔗 [LinkedIn](https://www.linkedin.com/in/aedwulf/)
