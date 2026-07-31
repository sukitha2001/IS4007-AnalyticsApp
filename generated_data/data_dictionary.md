# Data Dictionary — Revenue Analytics App (Dummy Dataset)

Synthetic data, 2023-01-01 to 2024-12-31. Randomly generated but built with
deliberate patterns so the required analyses (segmentation, forecasting,
discount impact, leakage) have real signal to uncover.

## 1. sales_transactions.csv (~12,900 rows)

| Field | Description |
|---|---|
| transaction_id | Unique transaction number |
| transaction_date | Date of sale |
| customer_id | FK → customers.csv |
| product_id | FK → products.csv |
| branch_id | One of 5 branches (North/South/East/West/Central) |
| channel | Online, Branch, Dealer, Direct Sales, Partner |
| quantity | Units sold (1–5) |
| unit_price | Selling price per unit, from product's standard_price |
| discount_percentage | Discount applied to this transaction |
| gross_revenue | quantity × unit_price |
| net_revenue | gross_revenue × (1 − discount_percentage/100) |
| cost | quantity × product's cost_price |
| gross_margin | net_revenue − cost |
| payment_status | Paid, Pending, Overdue, Partially Paid |

## 2. customers.csv (120 rows)

| Field | Description |
|---|---|
| customer_id | Unique customer identifier |
| customer_type | Individual, SME, Corporate |
| segment | Premium, Standard, Budget, New |
| acquisition_channel | Referral, Online, Walk-in, Sales Team |
| customer_since | Date joined |
| location_category | Urban, Suburban, Other |
| business_size | Small/Medium/Large (N/A for Individuals) |

## 3. products.csv (30 rows)

| Field | Description |
|---|---|
| product_id | Unique product identifier |
| product_name | Product name |
| category | Electronics, Home & Living, Apparel, Beauty & Personal Care, Sports & Outdoors, Office Supplies |
| standard_price | List price |
| cost_price | Cost to business |
| margin_percentage | (standard_price − cost_price) / standard_price |
| active_status | Active or Discontinued (2 discontinued products, phased out after Mar 2024) |

## 4. campaigns.csv (10 rows)

| Field | Description |
|---|---|
| campaign_id | Unique campaign identifier |
| campaign_name | Name of promotion |
| start_date / end_date | Campaign window |
| offer_type | Discount, Bundle, Cashback, Seasonal Offer |
| campaign_cost | Cost of running the campaign |

## Assumptions

- Daily transaction volume follows a Poisson process with a monthly seasonality
  multiplier (dip in Jun/Jul, strong ramp into Nov/Dec — simulates a holiday
  shopping pattern).
- Discount rates are higher during active campaign windows.
- SME customers are given a higher probability of Overdue/Pending payment
  status than Individual/Corporate customers (deliberate leakage signal —
  expect this to surface in Module 6).

## Deliberately embedded patterns (for you to "discover" in analysis)

1. **5 products** carry high revenue but thin margin (3–8%) — should surface
   as "high revenue, low profitability" in Module 3/6.
2. **3 products** are frequently over-discounted (20–30%) without a
   corresponding lift in quantity sold — a clean case for Module 4's
   discount-vs-volume analysis.
3. **10 customers** are flagged internally as high-value but stop
   transacting after mid-2024 — a reactivation-candidate cohort for Module 2
   (inactive customers) and Module 7 (recommendations).
4. **2 products** are discontinued and phase out of sales after March 2024.
5. **Seasonality**: revenue should show a visible Q4 uplift and a
   June/July soft patch — useful for Module 5 forecasting/decomposition.
6. **SME segment** carries disproportionate overdue payments — feeds Module 6
   (revenue leakage — overdue revenue).

Note: internal "helper" flags used to generate patterns #2 and #3 (e.g. which
customers were forced inactive) are not included as columns in the exported
files — they're meant to be *discovered* through your own RFM/inactivity and
discount-regression analysis, not read off directly.
