# FinPulse – Financial Analytics Dashboard (Power BI)

![Dashboard](assets/dashboard_preview.png)
![Profitability](assets/profitability_preview.png)

A two-page Power BI dashboard that analyses revenue, expenses and profit for a fictional business over **2022-2025** (24,699 transactions, 150 customers, 20 products, 4 departments, 4 sales channels).
The company "FinPulse" and all data are synthetic. The dataset is generated with a seeded Python script, so it is fully reproducible.

## Pages
**Dashboard:** Revenue, Expenses, Profit and Profit Margin KPIs with year-over-year change · Monthly Revenue vs Expenses · Revenue vs Budget · Revenue by Category · Revenue by Sales Channel · Department by Profitability · Year and Month slicers

**Profitability:** Top 5 customers by profit · Top 5 products by profit · Monthly profit trend · Profit margin % by category · Profit by region

## Key findings (2025)
| Metric | Result |
|---|---|
| Revenue | ₹256.8M, up 15.1% vs 2024 |
| Profit | ₹82.1M, margin 32.0% |
| Revenue vs budget | 2.7% below budget (₹256.8M vs ₹263.9M) |
| Top channel | Online, about 38% of revenue |
| Top category | Technology is 52% of revenue but has the lowest margin (24%) |
| Best margin | Software, 53% |
| Top product by profit | Laptop (₹13.7M) |

## Data model (star schema)
- `fact_transactions` (transaction_id, transaction_date, customer_id, product_id, quantity, sales_channel, payment_method, transaction_status, revenue, expenses)
- `dim_customers` (customer_id, customer_name, region, segment, state, city, country)
- `dim_products` (product_id, product_name, category, department, list_price)
- `budget` (year, month, department, budget_revenue, budget_expenses)
- `DimDate` and `DimDepartment` calculated tables

Only **Completed** transactions count towards revenue, expenses and profit.

## DAX highlights
All measures are in [`dax_measures.md`](dax_measures.md): year-over-year growth with `SAMEPERIODLASTYEAR`, budget variance, profit margin change in percentage points, and a dynamic top-category insight.

## Tools and skills
Power BI · Power Query · DAX (time intelligence) · Data modelling · Dashboard design · Python (pandas, NumPy) for synthetic data

## Repo structure
```
finpulse-powerbi-dashboard/
├── FinPulse_Dashboard.pbix
├── README.md
├── dax_measures.md
├── requirements.txt
├── data/      fact_transactions.csv, dim_customers.csv, dim_products.csv, budget.csv
├── scripts/   generate_data.py
├── theme/     FinPulse_Dark_Theme.json
└── assets/    dashboard_preview.png, profitability_preview.png, finpulse_sidebar_graphic.png
```

## Run it yourself
1. Open `FinPulse_Dashboard.pbix` in Power BI Desktop.
2. If Power BI asks for the data path: Home → Transform data → Data source settings → point to the `data/` folder.
3. To regenerate the data: `pip install -r requirements.txt` then `python scripts/generate_data.py` (seed 7).
4. Optional theme: View → Themes → Browse for themes → `theme/FinPulse_Dark_Theme.json`.

> Data is synthetic and for portfolio purposes only. The inspiration was a financial dashboard seen on LinkedIn; this project uses its own data, design and DAX.
