# DAX (FinPulse)

## Calculated tables
```dax
DimDate = ADDCOLUMNS(CALENDAR(DATE(2022,1,1),DATE(2025,12,31)),
  "Year",YEAR([Date]),"Month No",MONTH([Date]),"Month",FORMAT([Date],"MMM"))
```
```dax
DimDepartment = DISTINCT(SELECTCOLUMNS(dim_products,"department",dim_products[department]))
```
Calculated column on `budget`:
```dax
BudgetDate = DATE(budget[year], budget[month], 1)
```
Mark `DimDate` as date table, sort `Month` by `Month No`, set `Year` and `Month No` to "Don't summarize".

## Relationships
`dim_customers[customer_id]` → `fact_transactions[customer_id]` · `dim_products[product_id]` → `fact_transactions[product_id]` · `DimDate[Date]` → `fact_transactions[transaction_date]` · `DimDepartment[department]` → `dim_products[department]` · `DimDepartment[department]` → `budget[department]` · `DimDate[Date]` → `budget[BudgetDate]` (all one-to-many, single direction)

## Measures
```dax
Total Revenue = CALCULATE(SUM(fact_transactions[revenue]), fact_transactions[transaction_status] = "Completed")
Total Expenses = CALCULATE(SUM(fact_transactions[expenses]), fact_transactions[transaction_status] = "Completed")
Total Profit = [Total Revenue] - [Total Expenses]
Profit Margin % = DIVIDE([Total Profit], [Total Revenue])
Avg Order Value = DIVIDE([Total Revenue], CALCULATE(COUNTROWS(fact_transactions), fact_transactions[transaction_status] = "Completed"))

Revenue PY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(DimDate[Date]))
Expenses PY = CALCULATE([Total Expenses], SAMEPERIODLASTYEAR(DimDate[Date]))
Profit PY = CALCULATE([Total Profit], SAMEPERIODLASTYEAR(DimDate[Date]))
Revenue YoY % = DIVIDE([Total Revenue] - [Revenue PY], [Revenue PY])
Expenses YoY % = DIVIDE([Total Expenses] - [Expenses PY], [Expenses PY])
Profit YoY % = DIVIDE([Total Profit] - [Profit PY], [Profit PY])
Margin Change = [Profit Margin %] - DIVIDE([Profit PY], [Revenue PY])

Budget Revenue = SUM(budget[budget_revenue])
Budget Expenses = SUM(budget[budget_expenses])
Revenue vs Budget % = DIVIDE([Total Revenue] - [Budget Revenue], [Budget Revenue])

Top Category =
VAR _top = TOPN(1, VALUES(dim_products[category]), [Total Revenue], DESC)
VAR _name = MAXX(_top, dim_products[category])
VAR _share = DIVIDE(CALCULATE([Total Revenue], dim_products[category] = _name), [Total Revenue])
RETURN _name & ": " & FORMAT(_share, "0%") & " of revenue"
```
Create each measure separately in Power BI. YoY measures are blank for 2022 (no earlier year); the Year slicer is single-select so year-over-year is always meaningful.
