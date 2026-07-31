# Revenue Analytics App

## 1. Project Background

Businesses generate revenue through multiple products, customers, channels, branches, campaigns, and pricing decisions. However, many organizations struggle to clearly understand what drives revenue growth, where performance gaps exist, which customers are most valuable, and how future revenue may behave.

In this project, each group must build a Revenue Analytics Application using dummy business data. The application should help business users analyze revenue performance, identify commercial opportunities, and make evidence-based decisions.

## 2. Main Objective

To design and develop a revenue analytics app that uses statistical analysis to understand revenue performance, customer behavior, pricing impact, revenue leakage, and future revenue trends.

## 3. Requirement for All Groups

All groups must cover the full scope below.

Each group should include:

1. Revenue performance analysis
2. Customer segmentation and customer value analysis
3. Pricing, discount, and promotion analysis
4. Revenue forecasting
5. Revenue leakage or underperformance analysis
6. Business recommendations
7. Interactive revenue analytics app/dashboard
8. Final report and presentation

This means the groups should not be split by topic. Instead, each group will create its own complete solution.

---

## Expected Revenue Analytics App

### 1. App Purpose

The final application should act as a simple Revenue Analytics Command Center for a business user.

The user should be able to open the app and answer questions such as:

- How is revenue performing over time?
- Which products, customers, branches, or channels generate the most revenue?
- Which customers are high-value, medium-value, or low-value?
- Are discounts helping or hurting revenue?
- What revenue can be expected in the next few months?
- Where is revenue being lost or under-optimized?
- What actions should management take?

### 2. Suggested Tools for the App

Students may use any suitable tool, such as:

| Tool | Suitable For |
|---|---|
| Power BI | Dashboards and interactive business reporting |
| Tableau | Visual analytics and storytelling |
| Excel | Simple dashboards and statistical summaries |
| R Shiny | Statistical app development |
| Python Streamlit | Lightweight analytics app development |
| Python Dash | More customized dashboard app |
| Jupyter Notebook + widgets | Simple analytical prototype |

The expectation is not to build a production-grade software system. The app can be a functional prototype that clearly demonstrates the analytical thinking and business value.

---

## Suggested Dummy Dataset

The dummy dataset can represent a company selling products or services through multiple channels.

### 1. Sales Transaction Data

| Field | Description |
|---|---|
| transaction_id | Unique transaction number |
| transaction_date | Date of sale |
| customer_id | Customer identifier |
| product_id | Product or service identifier |
| branch_id | Branch or location identifier |
| channel | Online, branch, dealer, direct sales, partner |
| quantity | Quantity sold |
| unit_price | Selling price per unit |
| discount_percentage | Discount given |
| gross_revenue | Revenue before discount |
| net_revenue | Revenue after discount |
| cost | Estimated cost of product/service |
| gross_margin | Net revenue minus cost |
| payment_status | Paid, pending, overdue, partially paid |

### 2. Customer Data

| Field | Description |
|---|---|
| customer_id | Customer identifier |
| customer_type | Individual, SME, corporate |
| segment | Premium, standard, budget, new |
| acquisition_channel | Referral, online, walk-in, sales team |
| customer_since | Date customer joined |
| location_category | Urban, suburban, other |
| age_band or business_size | Optional customer attribute |

### 3. Product Data

| Field | Description |
|---|---|
| product_id | Product identifier |
| product_name | Product/service name |
| category | Product category |
| standard_price | Listed price |
| cost_price | Cost to business |
| margin_percentage | Product margin |
| active_status | Active or discontinued |

### 4. Campaign Data

| Field | Description |
|---|---|
| campaign_id | Campaign identifier |
| campaign_name | Name of promotion |
| start_date | Campaign start date |
| end_date | Campaign end date |
| offer_type | Discount, bundle, cashback, seasonal offer |
| campaign_cost | Cost of campaign |

---

## Minimum App Modules

Each group's app should contain the following sections.

### Module 1: Executive Revenue Dashboard

This section should summarize overall revenue performance.

Required outputs:

| Output | Example |
|---|---|
| Total revenue | Total net revenue for selected period |
| Revenue trend | Monthly or weekly revenue trend |
| Revenue by category | Revenue by product category |
| Revenue by channel | Online vs branch vs dealer sales |
| Revenue by branch | Branch/location performance |
| Gross margin | Revenue after estimated cost |
| Average order value | Net revenue divided by number of transactions |

### Module 2: Customer Analytics

This section should analyze customers and customer value.

Required outputs:

| Output | Example |
|---|---|
| Customer segmentation | High-value, medium-value, low-value customers |
| RFM analysis | Recency, frequency, monetary value |
| Customer lifetime value estimate | Estimated value of customers over time |
| Repeat purchase behavior | Customers buying more than once |
| Inactive customers | Customers who have not purchased recently |
| Top customers | Customers contributing most revenue |

Suggested methods:

- RFM analysis
- Cluster analysis
- Descriptive statistics
- Customer ranking
- Customer concentration analysis

### Module 3: Product and Channel Revenue Analysis

This section should identify which products and channels are driving or weakening revenue.

Required outputs:

| Output | Example |
|---|---|
| Top products | Highest revenue products |
| Low-performing products | Products with poor sales or margin |
| Category contribution | Revenue share by category |
| Channel comparison | Revenue and margin by sales channel |
| Branch/channel ranking | Best and weakest performing channels |

Suggested methods:

- Pareto analysis
- Contribution analysis
- Margin analysis
- Cross-tabulation
- Trend comparison

### Module 4: Pricing and Discount Analysis

This section should assess whether discounts are supporting revenue growth or reducing profitability.

Required outputs:

| Output | Example |
|---|---|
| Discount distribution | How discounts are spread across transactions |
| Revenue by discount band | Revenue at 0%, 5%, 10%, 15% discount etc. |
| Margin impact | Effect of discount on gross margin |
| Discount vs quantity sold | Whether discounts increase sales volume |
| Over-discounted products/customers | Cases where discounts reduce commercial value |

Suggested methods:

- Correlation analysis
- Regression analysis
- Hypothesis testing
- Margin comparison
- Before-and-after promotion analysis

### Module 5: Revenue Forecasting

This section should forecast future revenue.

Required outputs:

| Output | Example |
|---|---|
| Monthly revenue forecast | Forecast for next 3 to 6 months |
| Forecast chart | Historical revenue plus forecast |
| Forecast error | MAE, RMSE, or MAPE |
| Scenario view | Best case, base case, low case |

Suggested methods:

- Moving average
- Exponential smoothing
- Linear trend model
- Seasonal decomposition
- ARIMA, if suitable
- Regression-based forecasting

### Module 6: Revenue Leakage and Underperformance

This section should identify revenue gaps and missed opportunities.

Required outputs:

| Leakage Area | Example |
|---|---|
| Overdue revenue | Sales made but not collected |
| Excessive discounting | Discounts without enough revenue benefit |
| Low-margin sales | High revenue but low profitability |
| Inactive customers | Customers who stopped buying |
| Weak branches/channels | Areas below expected performance |
| Product underperformance | Products with poor revenue contribution |

Suggested methods:

- Exception reporting
- Threshold-based flags
- Aging analysis
- Margin leakage analysis
- Customer inactivity analysis

### Module 7: Recommendations Page

The app should include a final recommendations page.

This section should convert statistical findings into business actions.

Example recommendations:

| Finding | Recommendation |
|---|---|
| Certain customers are high value but inactive | Run targeted reactivation campaign |
| Some products sell well but have low margin | Review pricing or supplier cost |
| Discounts do not significantly increase volume | Reduce blanket discounting |
| One channel has high revenue but poor margin | Reassess commissions or operating cost |
| Revenue forecast shows seasonal dip | Plan campaigns before expected decline |
| Overdue payments are concentrated in one segment | Prioritize collections for that segment |

---

## Expected Deliverables

| Deliverable | Description |
|---|---|
| Revenue analytics app | Interactive dashboard or app using dummy/anonymized data |
| Dataset and data dictionary | Dataset used, field definitions, assumptions |
| Statistical analysis | Methods, tests, models, and outputs |
| Final report | Full explanation of analysis, findings, and recommendations |
| Final presentation | Business-style presentation of app and insights |
| Code/model files | R, Python, Excel, Power BI, Tableau, or other files |
| User guide | Short guide explaining how to use the app |

---

## Group Structure

Each group should ideally have 4 students.

Suggested internal role split:

| Role | Responsibility |
|---|---|
| Student 1 | Data preparation, data dictionary, quality checks |
| Student 2 | Exploratory analysis and revenue performance analysis |
| Student 3 | Statistical modelling, segmentation, forecasting |
| Student 4 | App/dashboard development and final presentation |

However, all students should understand the full project and be able to explain the methodology and findings.

---

## Suggested Final Report Structure

1. Executive summary
2. Business problem and project objective
3. Description of dummy dataset
4. Data preparation and assumptions
5. Revenue performance analysis
6. Customer segmentation analysis
7. Product and channel analysis
8. Pricing and discount analysis
9. Revenue forecasting
10. Revenue leakage and underperformance analysis
11. App design and functionality
12. Key findings
13. Business recommendations
14. Limitations
15. Conclusion
16. Appendix: code, formulas, statistical outputs, screenshots

---

## Suggested Final Presentation Structure

1. Project objective
2. Dataset overview
3. Key revenue trends
4. Customer and product insights
5. Pricing and discount findings
6. Forecasting results
7. Revenue leakage findings
8. Revenue Analytics App Demonstration
9. Business recommendations
10. Limitations and future improvements

---

## Minimum Acceptance Criteria

For the project to be considered complete, each group must submit:

1. A working revenue analytics app or dashboard
2. A dummy/anonymized dataset
3. A data dictionary
4. Statistical analysis outputs
5. A written report
6. A final presentation
7. A short app user guide

---

## Strong Final Project Statement

Each group will design and build a Revenue Analytics Application using dummy business data. The application should demonstrate how statistical methods can be used to analyze revenue performance, customer behavior, pricing decisions, forecasting, and revenue leakage, and translate those findings into practical business recommendations.

This makes the project more applied, practical, and showcase-friendly while still remaining aligned with a Statistics in Practice module.
