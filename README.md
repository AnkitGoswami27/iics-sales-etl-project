# IICS Sales ETL Pipeline — Campus Use Case
### HCL Campus Hackathon 2026 | Informatica Intelligent Cloud Services (CDI)

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-58a6ff?style=flat-square&logo=github)](https://ankitgoswami27.github.io/iics-sales-etl-project/)
[![Oracle SQL Guide](https://img.shields.io/badge/Also%20See-Oracle%20SQL%20%26%20PL%2FSQL%20Guide-orange?style=flat-square)](https://ankitgoswami27.github.io/oracle-sql-guide/)

---

## Project Overview

A complete, production-style cloud ETL pipeline built entirely on **Informatica Intelligent Cloud Services (CDI)**. The pipeline ingests raw retail sales data, applies business-rule-based data cleansing, computes revenue aggregations by product category, and orchestrates both stages through a Taskflow with conditional execution.

> Designed for the HCL Campus Hackathon use case: _"Design and implement an ETL solution for a retail sales analytics platform."_

---

## Live Project Showcase

**[View Full Showcase with Screenshots →](https://ankitgoswami27.github.io/iics-sales-etl-project/)**

---

## Pipeline Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     TF_Sales_Pipeline (Taskflow)                 │
│                                                                  │
│  ┌───────┐    ┌──────────────────────────┐    ┌───────────────┐  │
│  │ Start │───▶│  Step1_Cleanse           │───▶│ Step2_Category│  │
│  └───────┘    │  (MappingTask1)          │    │ (MT_Category) │  │
│               └──────────────────────────┘    └───────────────┘  │
│                    ↓ On Success only ↑                           │
└──────────────────────────────────────────────────────────────────┘

Mapping 1 — m_Clean_Dirty_Transactions
  sales_transactions_dirty.csv
       │
       ▼
  [exp_DataFixes]  ← Expression Transformation
  - ABS(TO_INTEGER(QUANTITY))         → Fix negatives
  - IIF(DISCOUNT < 0 OR > 100, 0, ..) → Fix invalid discounts
  - IS_DATE(TRANSACTION_DATE, ..)     → Validate dates
  - IIF(ISNULL(x) OR .., 'FAIL','PASS') → Reject flag
       │
       ▼
  [Router]
  ├── PASS ──▶ tgt_Cleaned_Transactions.csv
  └── FAIL ──▶ tgt_Rejected_Records.csv

Mapping 2 — m_Category_Summary
  sales_transactions.csv
       │
       ▼
  [exp_Revenue]
  - o_REVENUE = TO_DECIMAL(QUANTITY) * TO_DECIMAL(UNIT_PRICE)
                * (1 - TO_DECIMAL(DISCOUNT_PERCENT)/100)
       │
       ▼
  [agg_Category]  GROUP BY PRODUCT_ID
  - TOTAL_QUANTITY = SUM(TO_INTEGER(QUANTITY))
  - TOTAL_REVENUE  = SUM(o_REVENUE)
  - AVG_DISCOUNT   = AVG(TO_DECIMAL(DISCOUNT_PERCENT))
       │
       ▼
  TGT_CATEGORY_SUMMARY.csv
```

---

## Repository Structure

```
iics-sales-etl-project/
├── index.html                    # Showcase page (GitHub Pages)
├── README.md                     # This file
├── screenshots/
│   ├── 01_cleansing_mapping.png  # m_Clean_Dirty_Transactions canvas
│   ├── 02_expression_ports.png   # exp_DataFixes port configuration
│   ├── 03_category_mapping.png   # m_Category_Summary canvas
│   ├── 04_taskflow.png           # TF_Sales_Pipeline canvas
│   └── 05_jobs_success.png       # My Jobs — Success execution log
├── data/
│   ├── source/
│   │   ├── sales_transactions.csv        # 50 clean records (source for Mapping 2)
│   │   ├── sales_transactions_dirty.csv  # 40 dirty records (source for Mapping 1)
│   │   ├── customer_master.csv           # Customer reference data
│   │   └── product_master.csv            # Product reference data
│   └── output/
│       ├── CLEANED_DIRTY_TRANSACTIONS.csv  # Mapping 1 output — passed records
│       └── REJECTED_RECORDS.csv            # Mapping 1 output — rejected records
└── scripts/
    ├── generate_data.py            # Generates core source CSVs
    └── generate_source_data.py     # Generates full dataset (500K rows)
```

---

## Mappings Deep Dive

### Mapping 1: `m_Clean_Dirty_Transactions`

| Component | Type | Purpose |
|-----------|------|---------|
| Source | Flat File Reader | Reads `sales_transactions_dirty.csv` (40 rows) |
| `exp_DataFixes` | Expression | Applies 6 data quality rules via IIF/TO_INTEGER/IS_DATE |
| Router | Router | Splits PASS records from FAIL records |
| `tgt_Cleaned_Transactions` | Flat File Writer | Stores validated records |
| `tgt_Rejected_Records` | Flat File Writer | Stores records that failed validation |

**Parameters:**
| Parameter | Type | Direction | Purpose |
|-----------|------|-----------|---------|
| `LAST_EXTRACT_DATE` | String | Input | Watermark for incremental loads |
| `SOURCE_FILE_NAME` | String | Input | Parameterize source filename |
| `REJECT_COUNT` | Integer | In-Out | Count of rejected records passed back |

**Data Quality Rules in `exp_DataFixes`:**
```
o_QUANTITY    = ABS(TO_INTEGER(QUANTITY))
o_UNIT_PRICE  = IIF(TO_DECIMAL(UNIT_PRICE) < 0, 0, TO_DECIMAL(UNIT_PRICE))
o_DISCOUNT    = IIF(TO_DECIMAL(DISCOUNT_PERCENT) < 0 OR
                    TO_DECIMAL(DISCOUNT_PERCENT) > 100,
                    0, TO_DECIMAL(DISCOUNT_PERCENT))
o_CUSTOMER_ID = TO_INTEGER(CUSTOMER_ID)
o_DATE_FIXED  = IIF(IS_DATE(TRANSACTION_DATE,'MM/DD/YYYY'),
                    TO_DATE(TRANSACTION_DATE,'MM/DD/YYYY'), NULL)
o_REJECT_FLAG = IIF(ISNULL(CUSTOMER_ID) OR ISNULL(QUANTITY) OR
                    TO_INTEGER(QUANTITY) <= 0 OR
                    NOT IS_DATE(TRANSACTION_DATE,'MM/DD/YYYY'),
                    'FAIL', 'PASS')
```

---

### Mapping 2: `m_Category_Summary`

| Component | Type | Purpose |
|-----------|------|---------|
| Source | Flat File Reader | Reads `sales_transactions.csv` (50 clean rows) |
| `exp_Revenue` | Expression | Calculates revenue per row with discount applied |
| `agg_Category` | Aggregator | Groups by PRODUCT_ID, computes SUM/AVG |
| Target | Flat File Writer | Writes `TGT_CATEGORY_SUMMARY.csv` |

**Revenue Formula:**
```
o_REVENUE = TO_DECIMAL(QUANTITY) * TO_DECIMAL(UNIT_PRICE)
            * (1 - TO_DECIMAL(DISCOUNT_PERCENT) / 100)
```

**Aggregation Ports:**
```
TOTAL_QUANTITY = SUM(TO_INTEGER(QUANTITY))      [Group By: PRODUCT_ID]
TOTAL_REVENUE  = SUM(o_REVENUE)                 [Decimal(15,2)]
AVG_DISCOUNT   = AVG(TO_DECIMAL(DISCOUNT_PERCENT)) [Decimal(10,2)]
```

---

## Taskflow: `TF_Sales_Pipeline`

```
Start ──▶ Step1_Cleanse ──[On Success]──▶ Step2_Category ──▶ End
                       ──[On Failure]──▶ End (pipeline aborts)
```

- Step 1 must succeed before Step 2 executes — analytical reports are never built on uncleansed data
- Both steps are **Mapping Tasks** linked to their respective mappings
- Taskflow status: **Valid ✓** | Last run: **Mar 10, 2026 → SUCCESS** (2 subtasks)

---

## Execution Results

| Job | Status | Date | Records |
|-----|--------|------|---------|
| `TF_Sales_Pipeline` | ✅ Success | Mar 10, 2026 | 2 subtasks |
| `m_Clean_Dirty_Transactions` | ✅ Success | Mar 10, 2026 | 40 rows processed |
| `m_load_stg_sales_raw` | ✅ Success | Earlier run | **500,000 rows** |

---

## Data Generation

Source data was programmatically generated using Python to simulate real-world data quality issues:

```python
# generate_source_data.py generates:
# - sales_transactions.csv       (50 clean records)
# - sales_transactions_dirty.csv (40 records with injected errors)
# - customer_master.csv          (customer reference)
# - product_master.csv           (product reference)

# Injected data quality issues:
# - Negative quantities
# - Discount percentages > 100
# - NULL customer IDs
# - Invalid date formats
# - Missing unit prices
```

---

## Technologies Used

| Category | Technology |
|----------|-----------|
| ETL Platform | Informatica IICS CDI (Cloud Data Integration) |
| Runtime | Secure Agent — `AnkitGoswami` |
| Transformations | Expression, Router, Aggregator, Filter, Source, Target |
| Functions | TO_INTEGER, TO_DECIMAL, IIF, IS_DATE, ISNULL, ABS, SUM, AVG |
| File Format | Flat File (CSV) |
| Data Generation | Python 3 |
| Version Control | Git + GitHub |

---

## Key Learning Outcomes

- **Flat file type handling:** All CSV fields arrive as String in IICS — explicit `TO_DECIMAL()` / `TO_INTEGER()` conversion required before any arithmetic
- **Parameterized mappings:** Using Input and In-Out parameters for reusable, configurable pipelines
- **Conditional orchestration:** Taskflow On-Success links prevent downstream processing of bad data
- **Data quality design:** Separating cleansing from analytics into distinct mappings follows separation of concerns principle
- **Preparation enablement:** A concise quick-reference cheat sheet supports faster formula recall during timed implementation rounds

---

## Author

**Ankit Goswami** | IMS Engineering College  
HCL Campus Hackathon 2026

[Oracle SQL & PL/SQL Guide](https://ankitgoswami27.github.io/oracle-sql-guide/) | [GitHub Profile](https://github.com/AnkitGoswami27)
