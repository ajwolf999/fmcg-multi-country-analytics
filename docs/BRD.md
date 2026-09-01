# Business Requirements Document

## FMCG Multi-Country Category Analytics

## 1. Project Overview

This project delivers an end-to-end analytics capability for FMCG category
performance across 7 European markets. It processes multi-year transactional
sales data (2021–2023, 1.1M records) to support data-driven decision-making
in promotional strategy, seasonal inventory planning, and stockout risk
management. The deliverable includes a documented data pipeline, a validated
analytical data model, and an interactive dashboard for ongoing self-service
reporting.

## 2. Business Objectives

The analysis must enable category management stakeholders to:

1. **Evaluate promotional ROI** — determine whether promotional discounting
   generates sufficient volume uplift to offset margin loss, by category.
2. **Anticipate seasonal demand shifts** — identify predictable peak and trough
   periods to inform inventory and staffing decisions ahead of time.
3. **Quantify and prioritize stockout impact** — estimate revenue lost to
   stockouts and identify which markets should be prioritized for inventory
   planning improvements.

## 3. Scope

### In Scope

- Analysis of the Kaggle FMCG Multi-Country Sales dataset (1.1M transactions,
  2021–2023, 7 European countries)
- Python ETL pipeline loading raw CSV data into MySQL with explicit data typing
  (e.g., dates stored as DATE, not string) and chunked processing for memory efficiency
- Dimensional data model (star schema) with 4 dimension tables (date, store,
  product, supplier) and 1 fact table, eliminating data redundancy and supporting
  efficient multi-dimensional analysis
- 8-test data quality validation framework covering completeness, uniqueness,
  validity, business logic, and referential integrity
- Business analysis addressing three questions: promotional effectiveness,
  seasonal demand patterns, and stockout revenue impact
- Interactive Streamlit dashboard enabling filtering and exploration by country,
  category, and time period
- Public deployment via Streamlit Community Cloud

### Out of Scope

- Sales forecasting or predictive modeling (analysis is historical/descriptive only)
- Real-time or live data feeds (dataset is static, covering a fixed historical period)
- Supplier/procurement performance analysis (dataset's supplier data was identified
  as synthetic and unreliable during data quality profiling — see Finding in
  `data_quality_report.md`)
- Markets or countries outside the 7 represented in the source dataset
- Validation against real-world FMCG benchmarks (source data is synthetic, as
  documented in the Data Quality Report)

## 4. Stakeholders

| Role                              | Interest                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| Category Manager                  | Primary consumer of findings — uses promotional and seasonal insights to adjust category strategy |
| Supply Chain / Inventory Planning | Uses stockout and seasonal demand findings to inform replenishment policy                         |
| Commercial / Trade Marketing      | Uses promotional effectiveness findings to calibrate discount depth and campaign timing           |
| Data/Analytics Team               | Owns the underlying pipeline, data model, and dashboard for ongoing maintenance                   |

## 5. Functional Requirements

| ID    | Requirement                                                                                                        |
| ----- | ------------------------------------------------------------------------------------------------------------------ |
| FR-01 | System shall ingest FMCG sales data from CSV source into a relational database                                     |
| FR-02 | System shall validate data quality (nulls, duplicates, value ranges, referential integrity) before analysis        |
| FR-03 | System shall model data using a dimensional (star) schema to support efficient querying                            |
| FR-04 | System shall calculate promotional effectiveness metrics by category (units, revenue, margin — promo vs non-promo) |
| FR-05 | System shall identify seasonal demand patterns by month and year                                                   |
| FR-06 | System shall estimate stockout-related revenue loss by market                                                      |
| FR-07 | System shall provide an interactive dashboard with filtering by country and category                               |
| FR-08 | System shall be deployable and publicly accessible without requiring local setup                                   |

## 6. Success Criteria

- All three business questions (promotional effectiveness, seasonal demand,
  stockout impact) are answered with quantified findings, each traceable to
  a documented SQL query
- Data quality is validated and transparently documented — including known
  limitations (synthetic dataset) — so findings can be trusted within their
  stated scope
- The dashboard is intuitive enough for a non-technical stakeholder to navigate
  and explore without guidance
- The analytical methodology (data modeling, validation, and business logic)
  is sound and would apply equally to real transactional data

## 7. Assumptions & Constraints

### Assumptions

- The Kaggle dataset structure (columns, granularity, relationships) is
  representative enough of real FMCG transactional data to demonstrate valid
  analytical methodology, even though the values themselves are synthetic
- Findings and recommendations reflect patterns _within this dataset_ and are
  not intended to represent real-world FMCG market conditions or inform actual
  business decisions
- The dataset's structure (33 columns spanning time, store, product, sales,
  and supply chain dimensions) is sufficiently rich to support multi-theme
  analysis (promotions, seasonality, stockouts)

### Constraints

- GitHub's 100MB file size limit required reducing the deployed SQLite dataset
  (via column pruning and a 2-year date filter) from 1.1M to 733K rows — the
  full 3-year, 1.1M-row dataset remains available in the local MySQL environment
- Streamlit Community Cloud's free tier does not support a live MySQL connection,
  requiring a SQLite-based deployment architecture distinct from local development
- No access to a live/production data source — analysis is limited to the static
  historical CSV export
