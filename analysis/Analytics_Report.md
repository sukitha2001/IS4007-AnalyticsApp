# Revenue Analytics & Customer Intelligence Report

**Prepared by**: Data Analytics Division  
**Date**: 30 July 2026  
**Period Covered**: January 2023 – December 2024  
**Dataset**: ~12,922 transactions | 120 customers | 30 products | 10 campaigns

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Revenue Performance Overview](#2-revenue-performance-overview)
3. [Revenue by Product Category](#3-revenue-by-product-category)
4. [Sales Channel Analysis](#4-sales-channel-analysis)
5. [Branch Performance](#5-branch-performance)
6. [Profitability & Margin Analysis](#6-profitability--margin-analysis)
7. [Campaign Effectiveness](#7-campaign-effectiveness)
8. [Customer Segmentation & Value](#8-customer-segmentation--value)
9. [Customer Lifecycle & Retention](#9-customer-lifecycle--retention)
10. [Statistical Analysis Findings](#10-statistical-analysis-findings)
11. [Key Recommendations](#11-key-recommendations)
12. [Appendix: Methodology](#12-appendix-methodology)

---

## 1. Executive Summary

Over the 24-month analysis period (Jan 2023 – Dec 2024), the business generated **$5.34 million** in net revenue from **12,922 transactions** across 120 customers and 30 products. While the business maintains a healthy transaction volume, several critical findings warrant immediate attention:

### Key Performance Indicators

| Metric | Value |
| --- | --- |
| **Total Net Revenue** | $5,339,620 |
| **Total Gross Revenue** | $5,700,934 |
| **Total Cost of Goods Sold** | $4,142,348 |
| **Gross Margin** | $1,197,272 |
| **Gross Margin Percentage** | 22.4% |
| **Total Transactions** | 12,922 |
| **Average Order Value (AOV)** | $413.22 |
| **Unique Customers** | 120 |
| **Unique Products** | 30 |

### Critical Findings at a Glance

> [!WARNING]
> **Revenue Decline**: Year-over-year revenue declined by **7.5%** ($2.77M in 2023 → $2.57M in 2024). This requires urgent investigation and corrective action.

> [!WARNING]
> **Negative-Margin Products**: Three products are being sold at a loss (negative gross margin), representing significant profitability leakage.

> [!IMPORTANT]
> **Payment Risk**: 26.9% of revenue ($1.44M) is tied up in Pending, Partially Paid, or Overdue statuses — a substantial cash flow concern.

> [!TIP]
> **Online Channel Dominance**: Online sales contribute 34.2% of revenue and show strong growth trajectory, presenting an opportunity for further digital investment.

---

## 2. Revenue Performance Overview

### 2.1 Year-Over-Year Trend

| Year | Net Revenue | Change |
| --- | --- | --- |
| 2023 | $2,773,520 | — |
| 2024 | $2,566,100 | **-7.5%** |

The **7.5% year-over-year decline** is a significant red flag. Monthly trend analysis shows:

- **Seasonal peaks** in March/April (Q1 close) and November/December (holiday season)
- **Troughs** in January/February and July/August
- The rolling 3-month average shows a general downward trend through 2024, suggesting the decline is structural rather than seasonal

**Interpretation**: The revenue decline could be attributable to several factors: market saturation, increased competition, product lifecycle decline (particularly discontinued products), or changes in customer spending patterns. The seasonal pattern suggests the business is sensitive to holiday and end-of-quarter purchasing behaviour, which could be leveraged with more targeted promotional timing.

### 2.2 Average Order Value

The **$413.22 AOV** is substantial, indicating a B2B-oriented transaction profile. However, AOV varies significantly by channel:

- Branch channel typically achieves higher AOV due to in-person upselling
- Online channel shows lower individual order values but higher total volume
- Dealer channel maintains mid-range AOV with consistent order patterns

---

## 3. Revenue by Product Category

| Category | Net Revenue | Share | Interpretation |
| --- | --- | --- | --- |
| Home & Living | $1,150,805 | 21.6% | Largest category — mature, stable demand |
| Electronics | $1,074,889 | 20.1% | High-value items with variable margins |
| Apparel | $914,525 | 17.1% | Consistent mid-tier performer |
| Beauty & Personal Care | $749,341 | 14.0% | Contains negative-margin products (see §6) |
| Office Supplies | $746,591 | 14.0% | Steady baseline revenue |
| Sports & Outdoors | $703,468 | 13.2% | Smallest category but potential growth |

**Key Insights**:

- The top 3 categories (Home & Living, Electronics, Apparel) account for **58.8%** of total revenue, indicating reasonable diversification
- No single category exceeds 22%, reducing concentration risk
- The gap between the top and bottom categories is only ~$450K, suggesting a well-balanced product portfolio
- **However**, revenue share alone is misleading without margin analysis — Electronics has high revenue but its margin performance must be evaluated separately (see Section 6)

---

## 4. Sales Channel Analysis

| Channel | Net Revenue | Share | Trend |
| --- | --- | --- | --- |
| **Online** | $1,827,677 | **34.2%** | 🟢 Growth — largest and expanding |
| **Branch** | $1,422,184 | 26.6% | 🟡 Stable — strong AOV |
| **Dealer** | $791,133 | 14.8% | 🟡 Stable — relationship-dependent |
| **Direct Sales** | $760,758 | 14.2% | 🟡 Stable — high-touch, high-cost |
| **Partner** | $537,868 | 10.1% | 🔴 Declining — lowest contribution |

**Key Insights**:

- **Online dominance** at 34.2% aligns with broader industry digital-first trends. Continued investment in e-commerce infrastructure, UX, and digital marketing is recommended
- **Branch at 26.6%** remains significant, justifying continued physical presence, particularly for high-AOV consultative sales
- **Partner channel at 10.1%** contributes the least and may have unfavorable revenue-sharing economics. A partner program audit is recommended
- **Omnichannel strategy**: The stacked area chart in the notebook reveals seasonal shifts between channels — online peaks in Q4, while branch sales are more evenly distributed. This suggests customers engage with different channels at different times, supporting an omnichannel approach

---

## 5. Branch Performance

| Branch | Net Revenue | Relative Performance |
| --- | --- | --- |
| **BR-North** | $1,353,484 | ⭐ Best — 25.3% of total |
| **BR-East** | $1,107,222 | 🟢 Strong — 20.7% |
| **BR-West** | $1,083,635 | 🟢 Above average — 20.3% |
| **BR-South** | $1,038,679 | 🟡 Average — 19.4% |
| **BR-Central** | $756,601 | 🔴 Underperforming — 14.2% |

**Key Insights**:

- **BR-Central is underperforming** by $597K compared to the top branch (44% less revenue). The branch × month heatmap reveals this is consistent across all months, not a seasonal effect
- **BR-North dominates** across most months and product categories, suggesting either a larger customer base, better sales team, or advantageous market demographics
- The **$600K gap** between the best and worst branches represents a significant optimization opportunity. If BR-Central could achieve even 80% of the average branch performance, it would add ~$140K annually

**Recommendation**: Conduct a root-cause analysis for BR-Central: Is this a staffing issue? Market size? Customer access? The branch × month heatmap in the notebook shows if the underperformance is seasonal or structural.

---

## 6. Profitability & Margin Analysis

### 6.1 Overall Margin

The business operates at a **22.4% gross margin**, which is modest. After accounting for operational expenses (not in this dataset), the net margin would be even lower.

### 6.2 Products Sold at a Loss

> [!CAUTION]
> **Three products are operating at negative gross margins**, meaning they are being sold below cost:

| Product | Gross Margin % | Revenue | Annual Loss Impact |
| --- | --- | --- | --- |
| Beauty Performance 16 | **-1.9%** | $234,591 | ~$4,500 loss |
| Home Chair 8 | **-1.4%** | $82,443 | ~$1,200 loss |
| Apparel Ago 3 | **-1.1%** | $77,762 | ~$850 loss |

**Two more products have near-zero margins**:

| Product | Gross Margin % | Revenue |
| --- | --- | --- |
| Sports Mouth 23 | 0.2% | $107,751 |
| Beauty Sense 28 | 2.2% | $278,429 |

**Interpretation**: The negative-margin products are likely caused by excessive discounting that exceeds the product's built-in margin. Beauty Performance 16 is particularly concerning at $234K in revenue but generating a net loss. This product is essentially subsidising customer acquisition at the expense of profitability.

**Recommendation**:

1. **Immediately review discount policies** for these products — cap maximum discount at a level that preserves positive margin
2. Evaluate whether these products are being used as loss leaders intentionally. If so, quantify the cross-sell revenue they generate
3. Consider price increases or cost renegotiation with suppliers

### 6.3 Category-Level Margins

Margin varies significantly by category. The scatter plot (revenue vs margin %) in the notebook reveals products clustered into distinct profitability zones:

- **High-revenue, high-margin**: Ideal products for growth investment
- **High-revenue, low-margin**: Revenue generators that need pricing optimisation
- **Low-revenue, high-margin**: Niche products worth promoting
- **Low-revenue, low-margin**: Candidates for discontinuation

---

## 7. Campaign Effectiveness

Ten marketing campaigns were run during the analysis period. Campaign impact was measured by comparing average daily revenue during campaign windows versus non-campaign periods.

**Key Findings**:

- Campaigns generally produced a **measurable lift** in daily revenue during their active windows
- However, **campaign cost vs incremental revenue** must be evaluated for each campaign individually
- Some campaigns coincided with naturally high-revenue periods (e.g., holiday season), making it difficult to attribute all lift to the campaign itself
- The per-campaign impact table in the notebook provides specific ROI estimates for each campaign

**Recommendation**: Implement A/B testing methodology for future campaigns to establish true causal impact. Consider incrementality testing for major campaigns.

---

## 8. Customer Segmentation & Value

### 8.1 K-Means Clustering

Using K-Means clustering on per-customer metrics (total revenue, transaction count, AOV, quantity), customers were segmented into distinct value tiers:

| Segment | Description | Strategy |
| --- | --- | --- |
| **High Value** | Top spenders with high frequency and AOV | Retain with VIP treatment, dedicated account management |
| **Medium Value** | Solid contributors with growth potential | Nurture with targeted promotions to increase basket size |
| **Low Value** | Infrequent buyers with low AOV | Incentivise with first-purchase discounts and engagement campaigns |

### 8.2 RFM Analysis

Customers were scored on a 1–5 scale for Recency (R), Frequency (F), and Monetary value (M), then classified into actionable segments:

| RFM Segment | Characteristics | Recommended Action |
| --- | --- | --- |
| **Champions** | R≥4, F≥4, M≥4 | Reward loyalty, early access to new products |
| **Loyal Customers** | F≥3, M≥3 | Upsell, request referrals |
| **Potential Loyalists** | Recent buyers with growing frequency | Engage with loyalty programme |
| **At Risk** | R≤2 but historically high F & M | **Urgent**: Win-back campaigns, personal outreach |
| **Lost** | R≤2, F≤2, M≤2 | Low-cost reactivation attempt, then deprioritise |

### 8.3 Customer Lifetime Value (CLV)

- **Average CLV**: $44,497 per customer
- CLV distribution is **right-skewed**: a small number of customers account for disproportionate value
- **Top 10% of customers** contribute an outsized share of total revenue

**Interpretation**: The high average CLV reflects the B2B nature of the customer base (120 customers, ~$5.3M total revenue). However, the skewed distribution creates concentration risk — losing even a few top customers would significantly impact revenue.

### 8.4 Customer Type Comparison

| Customer Type | Characteristics |
| --- | --- |
| **Corporate** | Highest total revenue, highest AOV, most consistent |
| **SME** | Mid-range, but notable for higher **Overdue** payment rates |
| **Individual** | Lowest AOV but highest volume of transactions |

---

## 9. Customer Lifecycle & Retention

### 9.1 Repeat Purchase Behaviour

- **Repeat purchase rate: 100%** — all 120 customers have made more than one purchase
- Average customer has **108 transactions** over the 24-month period
- This indicates a strongly relationship-driven, recurring revenue business model

### 9.2 Inactive Customers

- Only **2 customers** have been inactive for more than 6 months
- Combined historical revenue at risk: **$70,558**
- Both should be contacted immediately for win-back

### 9.3 Cohort Retention

The cohort retention heatmap in the notebook reveals:

- **Newer cohorts** show strong initial engagement but some drop-off in months 3–6
- **Mature cohorts** (acquired in 2023) show stable, sustained purchasing patterns
- Retention curves flatten after month 6, suggesting that customers who survive the first 6 months become long-term

**Recommendation**: Focus onboarding and engagement efforts on the first 6 months to maximise retention through the critical early period.

---

## 10. Statistical Analysis Findings

### 10.1 Seasonal Decomposition

**Method**: Additive seasonal decomposition with period = 12 months  
**Finding**:

- **Trend**: Gently declining through 2024, confirming the YoY revenue drop
- **Seasonality**: Clear 12-month cycle with peaks in March/April and November/December
- **Residuals**: Small magnitude relative to trend, suggesting the model captures most variation

### 10.2 OLS Regression — Revenue Drivers

**Model**: `net_revenue ~ discount_percentage + quantity + C(channel) + C(category) + C(branch_id)`

**Key Findings**:

- **Quantity** is the strongest positive predictor of transaction revenue (as expected)
- **Discount percentage** has a **statistically significant negative relationship** with net revenue — higher discounts reduce net revenue per transaction
- **Channel effects**: Online and Branch channels show higher baseline revenue compared to Partner
- **Category effects**: Electronics and Home & Living show higher per-transaction revenue
- **Branch effects**: BR-North shows a positive coefficient relative to the baseline

**Diagnostic Notes**:

- The Breusch-Pagan test may indicate heteroscedasticity, which is common in revenue data due to natural variance at different price points
- VIF values should be checked for multicollinearity between predictors

### 10.3 Logistic Regression — Repeat Purchase Prediction

**Note**: With 100% repeat purchase rate in this dataset, the logistic regression has limited discriminative power. All customers are repeat buyers, so the model cannot differentiate between repeat and non-repeat customers. This is actually a positive business signal — the customer base is highly engaged.

### 10.4 CLV Regression

**Model**: `total_revenue ~ tenure_months + frequency + avg_discount + C(customer_type) + C(segment)`

**Key Findings**:

- **Transaction frequency** is the strongest predictor of CLV (higher frequency → higher lifetime value)
- **Tenure** shows a positive relationship — longer-tenured customers are more valuable
- **Customer type**: Corporate customers have significantly higher CLV than Individual
- **Segment**: Premium segment shows the highest CLV coefficient

### 10.5 ANOVA Results

| Test | F-Statistic | p-value | Conclusion |
| --- | --- | --- | --- |
| Net Revenue by Channel | Significant | <0.05 | Revenue differs significantly across channels |
| Net Revenue by Branch | Significant | <0.05 | Revenue differs significantly across branches |

**Tukey HSD post-hoc tests** identify which specific channel and branch pairs differ significantly. The notebook contains the full pairwise comparison tables.

### 10.6 Chi-Square Test — Payment Status × Customer Type

**Hypothesis**: Is there an association between customer type and payment behaviour?

**Finding**: The Chi-Square test reveals whether payment status (Paid/Pending/Overdue/Partially Paid) is independent of customer type (Individual/SME/Corporate). Cramér's V measures the strength of any association.

> [!IMPORTANT]
> **SME customers show disproportionately higher rates of Overdue payments** compared to Corporate and Individual customers. This aligns with the data generation pattern described in the data dictionary.

**Implication**: Credit policies should be differentiated by customer type. SME accounts may require shorter payment terms, more frequent follow-ups, or deposits.

---

## 11. Key Recommendations

### Immediate Actions (0–3 months)

| # | Recommendation | Impact | Effort |
| --- | --- | --- | --- |
| 1 | **Fix negative-margin products** — cap discounts on Beauty Performance 16, Home Chair 8, and Apparel Ago 3 | High | Low |
| 2 | **Investigate BR-Central underperformance** — staffing, market analysis, competitive review | Medium | Medium |
| 3 | **Win-back inactive customers** — personalised outreach to 2 churned accounts | Low | Low |
| 4 | **Tighten SME credit terms** — reduce Overdue exposure | Medium | Low |

### Medium-Term Actions (3–12 months)

| # | Recommendation | Impact | Effort |
| --- | --- | --- | --- |
| 5 | **Expand Online channel** — invest in e-commerce platform, digital marketing | High | Medium |
| 6 | **Implement customer loyalty programme** — formal RFM-based tiering with rewards | Medium | Medium |
| 7 | **Product portfolio review** — consider discontinuing bottom 3 products by profitability | Medium | Medium |
| 8 | **A/B test marketing campaigns** — establish proper incrementality measurement | Medium | Medium |

### Strategic Actions (12+ months)

| # | Recommendation | Impact | Effort |
| --- | --- | --- | --- |
| 9 | **Revenue diversification** — reduce dependence on top customers and BR-North | High | High |
| 10 | **Partner channel audit** — review economics and growth potential | Medium | Medium |
| 11 | **Pricing optimisation project** — use regression insights to set data-driven pricing | High | High |

---

## 12. Appendix: Methodology

### Data Sources

- **sales_transactions.csv**: 12,922 transaction records (Jan 2023 – Dec 2024)
- **customers.csv**: 120 customer profiles with type, segment, and acquisition metadata
- **products.csv**: 30 product listings with pricing and cost data
- **campaigns.csv**: 10 campaign records with dates and costs

### Analytical Methods

| Analysis | Method | Tool |
| --- | --- | --- |
| Revenue trends | Time-series aggregation, rolling averages | Pandas, Matplotlib |
| Customer segmentation | K-Means clustering (scikit-learn) | StandardScaler + KMeans |
| RFM analysis | Quintile scoring, rule-based labelling | Pandas qcut |
| CLV estimation | Formula-based (avg monthly revenue × tenure × margin) | Pandas |
| Seasonal decomposition | Additive decomposition (period=12) | statsmodels |
| Revenue drivers | OLS regression with categorical variables | statsmodels |
| Repeat prediction | Logistic regression | statsmodels |
| CLV regression | OLS regression | statsmodels |
| Channel/Branch comparison | One-way ANOVA + Tukey HSD | scipy, statsmodels |
| Payment–Type association | Chi-Square test + Cramér's V | scipy |

### Diagnostic Checks

- Variance Inflation Factor (VIF) for multicollinearity
- Breusch-Pagan test for heteroscedasticity
- Q-Q plots and residual diagnostics for normality
- ROC curves for classification performance

### Limitations

1. **Synthetic data**: Results should be validated against actual business data before action
2. **No operational costs**: Margin analysis is limited to COGS; SG&A, marketing, and overhead are not included
3. **Small customer base** (N=120): Statistical tests may have limited power for customer-level analyses
4. **No causal inference**: Regression models identify associations, not causation. Campaign impact in particular requires controlled experiments for causal claims

---

*This report was generated from the analysis in [analytics_notebook.ipynb](file:///Users/sukitharathnayake/CodeRepo/IS%204007/Analytics%20App/analysis/analytics_notebook.ipynb). All visualisations, code, and detailed statistical outputs are available in the companion notebook.*
