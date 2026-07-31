def get_module2_cells():
    cells = []

    # 1. Module 2 Header
    cells.append({
        "cell_type": "markdown",
        "source": """# Module 2: Customer Analytics & Statistical Modelling

This module provides a deep dive into customer behaviour, segmentation, and lifetime value, followed by rigorous statistical modelling to uncover the drivers of revenue and customer loyalty. 

**Business Context:** Understanding who our most valuable customers are, how they behave, and what factors influence their purchasing decisions is critical for targeted marketing, resource allocation, and strategic growth. By moving beyond simple descriptive statistics, we employ predictive modelling to anticipate future behaviour and optimise business outcomes. 

**Key Objectives:**
1. Segment the customer base to identify distinct profiles and value tiers.
2. Evaluate customer health and churn risk using RFM analysis.
3. Estimate Customer Lifetime Value (CLV) to guide acquisition investment.
4. Statistically test the significance of various business drivers on net revenue.
5. Build predictive models for repeat purchase behaviour."""
    })

    # 2. Customer Segmentation - K-Means
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.1 Customer Segmentation (K-Means Clustering)

We apply K-Means clustering to behavioral and monetary metrics to discover natural groupings within our customer base. The 'Elbow Method' helps us determine the optimal number of segments. This data-driven approach removes bias from pre-defined segmentations."""
    })

    cells.append({
        "cell_type": "code",
        "source": """# Aggregate customer metrics
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

customer_metrics = df.groupby('customer_id').agg(
    total_spend=('net_revenue', 'sum'),
    order_count=('transaction_id', 'nunique'),
    avg_order_value=('net_revenue', 'mean'),
    total_items=('quantity', 'sum')
).reset_index()

customer_metrics.fillna(0, inplace=True)
X = customer_metrics[['total_spend', 'order_count', 'avg_order_value']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow Plot
inertia = []
K_range = range(1, 10)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)

plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, marker='o', color=COLORS['primary'], linewidth=2)
plt.title('Elbow Method for Optimal K', fontsize=14)
plt.xlabel('Number of Clusters (k)', fontsize=12)
plt.ylabel('Inertia', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# K-Means with k=4
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
customer_metrics['cluster'] = kmeans.fit_predict(X_scaled)

plt.subplot(1, 2, 2)
sns.scatterplot(data=customer_metrics, x='order_count', y='total_spend', 
                hue='cluster', palette=COLORS['category_palette'][:optimal_k], s=80, alpha=0.8, edgecolor='white')
plt.title('Customer Segments: Spend vs. Order Count', fontsize=14)
plt.xlabel('Number of Orders', fontsize=12)
plt.ylabel('Total Spend', fontsize=12)
plt.legend(title='Cluster', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Profile Table
cluster_profile = customer_metrics.groupby('cluster').agg(
    customer_count=('customer_id', 'count'),
    avg_total_spend=('total_spend', 'mean'),
    avg_order_count=('order_count', 'mean'),
    avg_order_value=('avg_order_value', 'mean')
).round(2)
display(cluster_profile)

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("The Elbow Plot suggests a bend around k=3 or 4. We selected 4 clusters to capture nuanced behavior.")
print("The scatter plot reveals clear stratification based on purchase frequency and monetary value.")
print("- One cluster typically represents low-value, infrequent buyers (often the majority).")
print("- Another cluster captures high-frequency, high-spend 'Champions'.")
print("- The remaining clusters represent mid-tier customers with varying average order values.")
print("Business Implications: We should focus retention efforts on the high-spend cluster, attempt to upsell")
print("mid-tier customers, and minimize acquisition costs for the low-value segment unless they show growth potential.")
"""
    })

    # 3. RFM Analysis
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.2 RFM Analysis (Recency, Frequency, Monetary)

RFM analysis is a proven marketing technique used to quantitatively rank and group customers based on the recency, frequency, and monetary total of their recent transactions. This allows us to assign actionable labels (e.g., 'Champions', 'At Risk')."""
    })

    cells.append({
        "cell_type": "code",
        "source": """# Calculate RFM metrics
max_date = df['transaction_date'].max()

rfm = df.groupby('customer_id').agg(
    recency=('transaction_date', lambda x: (max_date - x.max()).days),
    frequency=('transaction_id', 'nunique'),
    monetary=('net_revenue', 'sum')
).reset_index()

# Quintiles (1-5, 5 is best for F/M, 1 is best for R)
# Reversing R so 5 is most recent
rfm['R_Score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')
rfm['F_Score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
rfm['M_Score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# Map to segments
def segment_customer(row):
    r, f, m = int(row['R_Score']), int(row['F_Score']), int(row['M_Score'])
    if (r >= 4) and (f >= 4) and (m >= 4): return 'Champions'
    if (r >= 3) and (f >= 3): return 'Loyal Customers'
    if (r >= 4) and (f <= 2): return 'Recent Customers'
    if (r <= 2) and (f >= 3): return 'At Risk'
    if (r <= 2) and (f <= 2): return 'Lost'
    return 'Others'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# Visualise
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart
segment_counts = rfm['Segment'].value_counts().sort_values(ascending=True)
ax[0].barh(segment_counts.index, segment_counts.values, color=COLORS['primary'], edgecolor='white', alpha=0.85)
ax[0].set_title('Customer Distribution by RFM Segment', fontsize=14)
ax[0].set_xlabel('Number of Customers', fontsize=12)

# Scatter (R vs F colored by Segment)
sns.scatterplot(data=rfm, x='recency', y='frequency', hue='Segment', 
                palette=COLORS['category_palette'], s=60, alpha=0.7, ax=ax[1], edgecolor='white')
ax[1].set_title('Recency vs Frequency by Segment', fontsize=14)
ax[1].invert_xaxis() # Most recent on the right
ax[1].set_xlabel('Recency (Days ago) -> More Recent', fontsize=12)
ax[1].set_ylabel('Frequency (Number of Orders)', fontsize=12)
ax[1].legend(bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

display(rfm.groupby('Segment').agg(
    Count=('customer_id', 'count'),
    Avg_Recency=('recency', 'mean'),
    Avg_Frequency=('frequency', 'mean'),
    Avg_Monetary=('monetary', 'mean')
).round(1).sort_values('Avg_Monetary', ascending=False))

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("The RFM analysis categorizes the customer base into actionable groups.")
print("1. 'Champions' buy often, spend the most, and purchased recently. They are prime candidates for early product releases.")
print("2. 'At Risk' customers purchased frequently in the past but haven't returned recently. Targeted reactivation campaigns are urgent here.")
print("3. 'Lost' customers have low recency, frequency, and monetary value. Reactivation may have low ROI.")
print("Retention Priorities: Implement win-back emails with aggressive discounts for the 'At Risk' segment, while nurturing 'Recent Customers' to become 'Loyal'.")
"""
    })

    # 4. CLV Estimation
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.3 Customer Lifetime Value (CLV) Estimation

CLV predicts the total net profit attributed to the entire future relationship with a customer. We estimate it here using a simplified historic model based on average monthly revenue and customer tenure. This metric is crucial for determining how much we can afford to spend on customer acquisition (CAC)."""
    })

    cells.append({
        "cell_type": "code",
        "source": """import numpy as np

# Estimate customer tenure and monthly revenue
cust_dates = df.groupby('customer_id')['transaction_date'].agg(['min', 'max'])
cust_dates['tenure_days'] = (cust_dates['max'] - cust_dates['min']).dt.days
cust_dates['tenure_months'] = np.where(cust_dates['tenure_days'] < 30, 1, cust_dates['tenure_days'] / 30)

clv_df = rfm.merge(cust_dates, on='customer_id')
clv_df['monthly_revenue'] = clv_df['monetary'] / clv_df['tenure_months']

# Simplified CLV: Assuming an average lifespan of 36 months (industry dependent)
assumed_lifespan_months = 36
clv_df['estimated_CLV'] = clv_df['monthly_revenue'] * assumed_lifespan_months

plt.figure(figsize=(14, 6))
sns.histplot(clv_df['estimated_CLV'], bins=50, color=COLORS['accent'], kde=True, edgecolor='white', alpha=0.85)
plt.title('Distribution of Estimated Customer Lifetime Value (CLV)', fontsize=14)
plt.xlabel('Estimated CLV', fontsize=12)
plt.ylabel('Count of Customers', fontsize=12)

# Mark the mean and 90th percentile
plt.axvline(clv_df['estimated_CLV'].mean(), color=COLORS['secondary'], linestyle='dashed', linewidth=2, label='Mean CLV')
plt.axvline(clv_df['estimated_CLV'].quantile(0.9), color=COLORS['warning'], linestyle='dashed', linewidth=2, label='90th Percentile')
plt.legend()
plt.tight_layout()
plt.show()

# Merge with customer data if available to see CLV by segment
if 'segment' in customers.columns:
    merged_clv = clv_df.merge(customers[['customer_id', 'segment']], on='customer_id', how='left')
    clv_by_segment = merged_clv.groupby('segment')['estimated_CLV'].mean().sort_values(ascending=False)
    print("Average CLV by Customer Segment:")
    display(clv_by_segment.to_frame().round(2))

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("The CLV distribution is typically right-skewed, meaning a small percentage of customers account for a disproportionately large share of future revenue.")
print("The dashed lines highlight the mean and the 90th percentile top spenders.")
print("High-Value Characteristics: Customers above the 90th percentile represent our core asset.")
print("Investment Priorities: The average CLV sets a hard upper bound on allowable Customer Acquisition Cost (CAC).")
print("If specific segments (e.g., 'Premium') show significantly higher CLV, acquisition budgets should be reallocated to target similar profiles.")
"""
    })

    # 5. Repeat Purchase Behaviour
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.4 Repeat Purchase Behaviour

A healthy business relies on recurring revenue. Here, we analyze the distribution of purchase counts and compare the value generated by repeat buyers versus one-time buyers."""
    })

    cells.append({
        "cell_type": "code",
        "source": """order_counts = df.groupby('customer_id')['transaction_id'].nunique()
repeat_buyers = order_counts[order_counts > 1].count()
total_buyers = order_counts.count()
repeat_rate = repeat_buyers / total_buyers

plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
order_counts_clipped = order_counts.clip(upper=10) # Clip long tail for visualization
sns.countplot(x=order_counts_clipped, color=COLORS['primary'], edgecolor='white', alpha=0.85)
plt.title('Distribution of Number of Purchases per Customer', fontsize=14)
plt.xlabel('Number of Purchases (10 = 10+)', fontsize=12)
plt.ylabel('Count of Customers', fontsize=12)

plt.subplot(1, 2, 2)
revenue_split = pd.DataFrame({
    'Type': np.where(df['customer_id'].map(order_counts) > 1, 'Repeat Buyer', 'One-time Buyer'),
    'Revenue': df['net_revenue']
}).groupby('Type')['Revenue'].sum()

plt.pie(revenue_split, labels=revenue_split.index, autopct='%1.1f%%', 
        colors=[COLORS['accent'], COLORS['text_muted']], startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5, 'alpha': 0.85})
plt.title(f'Revenue Contribution (Repeat Rate: {repeat_rate:.1%})', fontsize=14)

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"The repeat purchase rate is {repeat_rate:.1%}, meaning {repeat_rate:.1%} of customers have bought more than once.")
print("The countplot shows a steep drop-off after the first purchase. Converting first-time buyers into second-time buyers is a major hurdle.")
print("However, the pie chart typically shows that repeat buyers contribute a massive share of total revenue.")
print("Loyalty Health: A strong core of repeat buyers stabilizes cash flow and reduces reliance on constant, expensive acquisition.")
print("Action: Implement aggressive 'second purchase' incentives (e.g., immediate discount on next order) to steepen the retention curve.")
"""
    })

    # 6. Inactive Customers
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.5 Inactive Customer Identification (Churn Risk)

We define 'inactive' customers as those who haven't made a purchase in the last 6 months (180 days). Identifying high-value customers who have recently gone dormant is critical for proactive churn prevention."""
    })
    
    cells.append({
        "cell_type": "code",
        "source": """inactivity_threshold_days = 180
inactive_customers = rfm[rfm['recency'] > inactivity_threshold_days]

# Cross-reference with Monetary value to find high-value churners
# Let's say high-value is M_Score >= 4
high_value_inactive = inactive_customers[inactive_customers['M_Score'].astype(int) >= 4]

plt.figure(figsize=(14, 6))
sns.histplot(inactive_customers['monetary'], bins=40, color=COLORS['danger'], kde=False, edgecolor='white', alpha=0.85, label='All Inactive')
if not high_value_inactive.empty:
    sns.histplot(high_value_inactive['monetary'], bins=40, color=COLORS['warning'], kde=False, edgecolor='white', alpha=0.85, label='High-Value Inactive')

plt.title('Revenue at Risk: Historic Spend of Inactive Customers (>6 months)', fontsize=14)
plt.xlabel('Historic Monetary Value', fontsize=12)
plt.ylabel('Number of Inactive Customers', fontsize=12)
plt.legend()
plt.tight_layout()
plt.show()

revenue_at_risk = high_value_inactive['monetary'].sum()
print(f"Number of inactive customers: {len(inactive_customers)}")
print(f"Number of high-value inactive customers: {len(high_value_inactive)}")
print(f"Total revenue generated by high-value inactive customers historically: ${revenue_at_risk:,.2f}")

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"We have identified {len(high_value_inactive)} 'high-value' customers who have been inactive for over {inactivity_threshold_days} days.")
print(f"These customers historically generated ${revenue_at_risk:,.2f}. This is significant revenue at risk.")
print("Churn Severity: While some churn is natural, losing top-tier customers severely impacts the bottom line.")
print("Reactivation Priorities: These high-value inactive profiles should be assigned to account managers for personalized outreach.")
print("We need to understand *why* they left (e.g., pricing, service issue, competitor) to prevent further leakage.")
"""
    })

    # 7. Customer Type Profiling
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.6 Customer Type Profiling

We analyze the performance metrics (Revenue, Average Order Value) across different customer types (e.g., Individual, SME, Corporate) to understand structural differences in purchasing power and behavior."""
    })
    
    cells.append({
        "cell_type": "code",
        "source": """# df already contains customer columns from the initial merge
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
sns.boxplot(data=df, x='customer_type', y='net_revenue', 
            palette=COLORS['category_palette'], showfliers=False,
            boxprops={'alpha': 0.85})
plt.title('Net Revenue per Transaction by Customer Type', fontsize=14)
plt.xlabel('Customer Type', fontsize=12)
plt.ylabel('Net Revenue (Outliers Hidden)', fontsize=12)

plt.subplot(1, 2, 2)
agg_type = df.groupby('customer_type').agg(
    Total_Revenue=('net_revenue', 'sum'),
    Average_Order_Value=('net_revenue', 'mean')
).reset_index()

sns.barplot(data=agg_type, x='customer_type', y='Total_Revenue', 
            palette=COLORS['category_palette'], edgecolor='white', alpha=0.85)
plt.title('Total Net Revenue by Customer Type', fontsize=14)
plt.xlabel('Customer Type', fontsize=12)
plt.ylabel('Total Revenue', fontsize=12)

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("The boxplots highlight the variance in Average Order Value (AOV) across customer types.")
print("Corporate clients typically display higher AOV and higher variance compared to Individual buyers.")
print("The total revenue bar chart shows the aggregate value of each segment.")
print("Resource Allocation: If Corporate/SME clients drive the bulk of revenue with high AOV, B2B sales teams should receive priority resourcing.")
print("Conversely, if Individual volume drives the business, mass-market digital advertising is the optimal strategy.")
"""
    })

    # 8. Acquisition Channel Analysis
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.7 Acquisition Channel Efficiency

Which marketing channels bring in the most valuable customers? We look at aggregate revenue and CLV by the channel through which the customer was originally acquired."""
    })
    
    cells.append({
        "cell_type": "code",
        "source": """if 'acquisition_channel' in customers.columns:
    if 'estimated_CLV' in clv_df.columns:
        clv_channel = clv_df.merge(customers[['customer_id', 'acquisition_channel']], on='customer_id')
        
        plt.figure(figsize=(14, 6))
        sns.barplot(data=clv_channel, x='acquisition_channel', y='estimated_CLV', 
                    estimator=np.mean, errorbar=('ci', 95), 
                    palette=COLORS['category_palette'], edgecolor='white', alpha=0.85)
        
        plt.title('Average Estimated CLV by Acquisition Channel', fontsize=14)
        plt.xlabel('Acquisition Channel', fontsize=12)
        plt.ylabel('Average Estimated CLV', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("This chart visualises the long-term value of customers acquired through different channels. The error bars represent the 95% confidence interval.")
print("Some channels may generate high volume but low-quality, low-CLV customers (e.g., discount affiliates).")
print("Other channels might bring fewer, but highly valuable customers (e.g., Direct Sales or Referrals).")
print("Where to Invest: Acquisition budgets should be heavily skewed towards the channels yielding the highest average CLV, assuming the Customer Acquisition Cost (CAC) for those channels remains viable.")
"""
    })

    # 9. Cohort Analysis
    cells.append({
        "cell_type": "markdown",
        "source": """## 2.8 Cohort Analysis (Retention Over Time)

Cohort analysis groups customers by the month of their first purchase. By tracking these cohorts over time, we can visualize retention curves and spot changes in customer quality or product stickiness over time."""
    })
    
    cells.append({
        "cell_type": "code",
        "source": """# Create cohort month
df['order_month'] = df['transaction_date'].dt.to_period('M')
df['cohort_month'] = df.groupby('customer_id')['transaction_date'].transform('min').dt.to_period('M')

# Group by cohort and order month, count unique customers
cohort_data = df.groupby(['cohort_month', 'order_month'])['customer_id'].nunique().reset_index()

# Calculate periods elapsed
cohort_data['period_number'] = (cohort_data['order_month'] - cohort_data['cohort_month']).apply(lambda x: x.n)

# Pivot table for retention counts
cohort_counts = cohort_data.pivot(index='cohort_month', columns='period_number', values='customer_id')

# Calculate retention rates (divide by period 0)
cohort_sizes = cohort_counts.iloc[:, 0]
retention = cohort_counts.divide(cohort_sizes, axis=0)

plt.figure(figsize=(16, 8))
sns.heatmap(retention, annot=True, fmt='.0%', cmap='Blues', 
            vmin=0.0, vmax=0.5, cbar_kws={'label': 'Retention Rate'})
plt.title('Customer Retention Heatmap by Monthly Cohorts', fontsize=14)
plt.ylabel('Cohort Month', fontsize=12)
plt.xlabel('Months Since First Purchase', fontsize=12)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("The cohort heatmap tracks retention over time. Month 0 is always 100%.")
print("Drop-off Patterns: The sharpest drop typically occurs between Month 0 and Month 1, representing buyers who never return.")
print("Cohort Quality: Reading down the columns allows us to compare cohorts. Are newer cohorts retaining better than older ones?")
print("If retention is worsening in newer cohorts, it suggests declining product quality, poorer customer service, or acquiring lower-intent customers.")
print("Action: Focus on onboarding experiences in Month 0 to boost Month 1 retention.")
"""
    })

    # SECTION B: Statistical Analysis
    cells.append({
        "cell_type": "markdown",
        "source": """# Section B: Rigorous Statistical Analysis

This section moves beyond descriptive visualizations to establish statistical significance. We utilize time-series decomposition, Ordinary Least Squares (OLS) regression, Logistic Regression, and ANOVA to quantify the relationships between variables, prove causality where possible, and provide statistically sound recommendations."""
    })

    # 11. Seasonal Decomposition
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.1 Time-Series Seasonal Decomposition

We decompose the aggregate daily revenue into three components: Trend, Seasonality, and Residuals (noise). This helps isolate underlying growth from regular cyclical patterns."""
    })
    
    cells.append({
        "cell_type": "code",
        "source": """from statsmodels.tsa.seasonal import seasonal_decompose

# Aggregate daily revenue
daily_revenue = df.groupby(df['transaction_date'].dt.date)['net_revenue'].sum()
daily_revenue.index = pd.to_datetime(daily_revenue.index)
daily_revenue = daily_revenue.asfreq('D').fillna(0) # Ensure continuous daily frequency

# Decompose (assuming additive model with a weekly or yearly period, let's use 30 days for monthly patterns if > 2 months data)
# Note: Period depends on data length. We'll try period=30 or 7.
try:
    decomposition = seasonal_decompose(daily_revenue, model='additive', period=30)
    
    fig = decomposition.plot()
    fig.set_size_inches(14, 10)
    fig.axes[0].set_title('Seasonal Decomposition of Daily Net Revenue (Additive, Period=30)', fontsize=14)
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"Could not perform seasonal decompose: {e}")

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("Decomposition separates the noise from the signal.")
print("1. Trend: Shows the overarching direction of revenue, smoothing out daily fluctuations. Is it growing or declining?")
print("2. Seasonal: Highlights repeating patterns. Consistent peaks suggest strong cyclicality (e.g., mid-month payroll effects or seasonal buying).")
print("3. Resid: The residual noise. High variance here means the business is highly unpredictable and volatile, subject to exogenous shocks.")
"""
    })

    # 12. OLS Regression - Revenue Drivers
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.2 OLS Regression: Drivers of Net Revenue

What fundamentally drives transaction value? We use an OLS regression to quantify the impact of discounts, quantity, channel, and branch on net revenue, controlling for multiple variables simultaneously."""
    })

    cells.append({
        "cell_type": "code",
        "source": """import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ── Prepare data ─────────────────────────────────────────────────────────────
reg_df = df.dropna(subset=['net_revenue', 'discount_percentage', 'quantity', 'channel', 'branch_id']).copy()

# ── Original (unstandardised) OLS ────────────────────────────────────────────
formula = "net_revenue ~ discount_percentage + quantity + C(channel) + C(branch_id)"
model_ols = smf_ols(formula, data=reg_df).fit()
print("═" * 70)
print("  ORIGINAL OLS — coefficients in natural units")
print("═" * 70)
print(model_ols.summary())

# ── Standardised OLS (z-score continuous predictors only) ─────────────────────
# Dummies (channel, branch) stay 0/1 — scaling binary variables is meaningless.
# Only continuous predictors are standardised so their coefficients are directly
# comparable in 'standard deviation units'.
from sklearn.preprocessing import StandardScaler

cont_vars = ['discount_percentage', 'quantity']
scaler = StandardScaler()
reg_df_std = reg_df.copy()
reg_df_std[cont_vars] = scaler.fit_transform(reg_df[cont_vars])

for v in cont_vars:
    print(f"  {v}: mean={reg_df[v].mean():.4f}, std={reg_df[v].std():.4f}  → z-scored")

formula_std = "net_revenue ~ discount_percentage + quantity + C(channel) + C(branch_id)"
model_ols_std = smf_ols(formula_std, data=reg_df_std).fit()

print()
print("═" * 70)
print("  STANDARDISED OLS — coefficients in standard-deviation units")
print("  Interpretation: β = change in net_revenue for 1 SD increase in predictor")
print("═" * 70)
print(model_ols_std.summary())

# ── Standardised coefficient comparison plot ──────────────────────────────────
# Keep only the two continuous vars for a clean apples-to-apples comparison.
coef_std = model_ols_std.params.drop('Intercept')
err_std  = model_ols_std.bse.drop('Intercept')

# Label cleanup
labels = [c.replace('C(channel)[T.', 'Channel: ').replace(']', '')
           .replace('C(branch_id)[T.', 'Branch: ')
           .replace('discount_percentage', 'Discount % (std)')
           .replace('quantity', 'Quantity (std)')
          for c in coef_std.index]

colors_bar = [COLORS['secondary'] if v < 0 else COLORS['primary'] for v in coef_std.values]

fig, ax = plt.subplots(figsize=(12, max(5, len(coef_std) * 0.45)))
ax.barh(labels, coef_std.values, xerr=1.96 * err_std.values,
        color=colors_bar, alpha=0.85, edgecolor='white', capsize=4)
ax.axvline(0, color='#1F2937', linewidth=1.2, linestyle='--')
ax.set_xlabel('Coefficient (standardised continuous, original dummy scale)')
ax.set_title('OLS — Standardised Coefficient Plot (95% CI; blue=positive, red=negative)', pad=12)
ax.grid(axis='x', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.show()

# ── Diagnostic Plots (2x2) on standardised model ─────────────────────────────
fig, ax = plt.subplots(2, 2, figsize=(14, 10))
sns.residplot(x=model_ols_std.fittedvalues, y=model_ols_std.resid, lowess=True,
              scatter_kws={'alpha': 0.3, 'color': COLORS['primary']},
              line_kws={'color': COLORS['secondary']}, ax=ax[0, 0])
ax[0, 0].set_title('Residuals vs Fitted')
ax[0, 0].set_xlabel('Fitted values')
ax[0, 0].set_ylabel('Residuals')

sm.qqplot(model_ols_std.resid, fit=True, line='45', ax=ax[0, 1], alpha=0.3, color=COLORS['primary'])
ax[0, 1].set_title('Normal Q-Q')

sns.histplot(model_ols_std.resid, kde=True, ax=ax[1, 0], color=COLORS['accent'], edgecolor='white')
ax[1, 0].set_title('Histogram of Residuals')

sns.regplot(x=model_ols_std.fittedvalues, y=np.sqrt(np.abs(model_ols_std.resid)), lowess=True,
            scatter_kws={'alpha': 0.3, 'color': COLORS['primary']},
            line_kws={'color': COLORS['secondary']}, ax=ax[1, 1])
ax[1, 1].set_title('Scale-Location')
ax[1, 1].set_xlabel('Fitted values')
ax[1, 1].set_ylabel('sqrt(|Residuals|)')

plt.tight_layout()
plt.show()

# ── VIF on continuous predictors only ─────────────────────────────────────────
X_vif = reg_df_std[cont_vars].copy()
X_vif = sm.add_constant(X_vif)
vif_data = pd.DataFrame({
    'Feature': X_vif.columns,
    'VIF': [variance_inflation_factor(X_vif.values, i) for i in range(X_vif.shape[1])]
}).query("Feature != 'const'")
print("── VIF (continuous predictors) ──")
print(vif_data.to_string(index=False))
print("  VIF < 5: low multicollinearity  |  VIF 5-10: moderate  |  VIF > 10: high")

print()
print('─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("ORIGINAL OLS — coefficients are in natural units (dollars per %, dollars per unit, etc.).")
print("  → Useful for asking: what happens if I give 1 more % discount or sell 1 more unit?")
print("")
print("STANDARDISED OLS — continuous predictors are z-scored (mean=0, SD=1).")
print("  → NOW you can compare: which matters more, discounting or quantity?")
print("  → The predictor with the largest |β| has the biggest effect per SD of variation.")
print("  → Dummy coefficients (channel, branch) retain their original unit scale.")
print("")
print("COEFFICIENT PLOT:")
print("  → Blue bars = positive effect on revenue. Red bars = negative effect.")
print("  → Bars that do NOT cross zero are statistically significant at ~95% CI.")
print("  → Compare bar lengths of 'Discount % (std)' vs 'Quantity (std)' directly.")
print("")
print("DIAGNOSTICS: Non-random patterns in Residuals vs Fitted suggest non-linearity.")
print("Deviations in the Q-Q plot indicate non-normal errors (common with skewed revenue data).")
"""
    })

    # 13. Logistic Regression - Repeat Purchase
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.3 Logistic Regression: Predicting Repeat Purchase

We frame loyalty as a binary classification problem: Did the customer buy more than once? We use logistic regression to understand which attributes increase the odds of a customer becoming a repeat buyer."""
    })

    cells.append({
        "cell_type": "code",
        "source": """from sklearn.metrics import classification_report, roc_curve, auc

if 'customer_type' in customers.columns:
    # ── Build customer-level data ─────────────────────────────────────────────
    logit_df = df.copy()
    counts = logit_df.groupby('customer_id')['transaction_id'].transform('nunique')
    logit_df['is_repeat'] = (counts > 1).astype(int)
    logit_df = logit_df.drop_duplicates(subset=['customer_id'])
    logit_df['tenure_days'] = (analysis_date - logit_df['customer_since']).dt.days

    # ── Original (unstandardised) Logistic ────────────────────────────────────
    logit_formula = "is_repeat ~ C(customer_type) + C(segment) + tenure_days"
    try:
        model_logit = smf_logit(logit_formula, data=logit_df).fit(disp=0)
        print("═" * 70)
        print("  ORIGINAL LOGISTIC — tenure_days in raw days")
        print("═" * 70)
        print(model_logit.summary())

        odds_orig = pd.DataFrame({
            'Odds Ratio': np.exp(model_logit.params),
            'p-value': model_logit.pvalues
        }).round(4)
        print("--- Original Odds Ratios ---")
        print(odds_orig.to_string())

        # ── Standardised Logistic (z-score tenure_days only) ──────────────────
        # Categorical dummies (customer_type, segment) stay 0/1 unchanged.
        logit_df_std = logit_df.copy()
        tenure_mean = logit_df['tenure_days'].mean()
        tenure_std  = logit_df['tenure_days'].std()
        logit_df_std['tenure_days'] = (logit_df['tenure_days'] - tenure_mean) / tenure_std
        print(f"  tenure_days standardised: mean={tenure_mean:.1f} days, SD={tenure_std:.1f} days")
        print("  Standardised coefficient = change in log-odds per 1 SD of tenure")

        model_logit_std = smf_logit(logit_formula, data=logit_df_std).fit(disp=0)
        print()
        print("═" * 70)
        print("  STANDARDISED LOGISTIC — tenure_days z-scored")
        print("  Odds ratios now on comparable scale across all predictors")
        print("═" * 70)
        print(model_logit_std.summary())

        odds_std = pd.DataFrame({
            'Odds Ratio': np.exp(model_logit_std.params),
            '95% CI Lower': np.exp(model_logit_std.conf_int()[0]),
            '95% CI Upper': np.exp(model_logit_std.conf_int()[1]),
            'p-value': model_logit_std.pvalues
        }).round(4).drop('Intercept', errors='ignore')
        print("--- Standardised Odds Ratios (with 95% CI) ---")
        print(odds_std.to_string())

        # ── Odds Ratio Forest Plot ─────────────────────────────────────────────
        or_vals  = np.exp(model_logit_std.params.drop('Intercept', errors='ignore'))
        ci_lower = np.exp(model_logit_std.conf_int().drop('Intercept', errors='ignore')[0])
        ci_upper = np.exp(model_logit_std.conf_int().drop('Intercept', errors='ignore')[1])

        labels_or = [c.replace('C(customer_type)[T.', 'CustType: ').replace(']', '')
                      .replace('C(segment)[T.', 'Segment: ')
                      .replace('tenure_days', 'Tenure (std)')
                     for c in or_vals.index]

        fig, ax = plt.subplots(figsize=(10, max(4, len(or_vals) * 0.55)))
        y_pos = range(len(or_vals))
        ax.scatter(or_vals.values, y_pos, color=COLORS['primary'], s=80, zorder=3)
        for i, (lo, hi) in enumerate(zip(ci_lower.values, ci_upper.values)):
            ax.hlines(i, lo, hi, color=COLORS['primary'], linewidth=2.5, alpha=0.7)
        ax.axvline(1.0, color=COLORS['secondary'], linewidth=1.5, linestyle='--', label='OR = 1 (no effect)')
        ax.set_yticks(list(y_pos))
        ax.set_yticklabels(labels_or, fontsize=9)
        ax.set_xlabel('Odds Ratio (95% CI)  |  OR > 1 increases repeat likelihood')
        ax.set_title('Logistic Regression — Standardised Odds Ratio Forest Plot (tenure z-scored; dummies on 0/1 scale)', pad=12)
        ax.legend()
        ax.grid(axis='x', linestyle='--', alpha=0.4)
        plt.tight_layout()
        plt.show()

        # ── ROC Curve ─────────────────────────────────────────────────────────
        preds = model_logit_std.predict(logit_df_std)
        fpr, tpr, _ = roc_curve(logit_df_std['is_repeat'], preds)
        roc_auc = auc(fpr, tpr)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color=COLORS['primary'], lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
        plt.plot([0, 1], [0, 1], color='grey', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0]); plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve — Repeat Purchase Logistic Model')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        plt.show()

    except Exception as e:
        print(f"Could not fit logistic regression: {e}")

print()
print('─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("ORIGINAL LOGISTIC: tenure_days coefficient = change in log-odds per 1 extra day.")
print("  → Hard to compare to dummy coefficients (days vs 0/1).")
print("")
print("STANDARDISED LOGISTIC: tenure_days is z-scored (1 unit = 1 SD ≈ ~several months).")
print("  → NOW the tenure OR is directly comparable in magnitude to dummy ORs.")
print("  → OR > 1: that attribute makes repeat purchase MORE likely.")
print("  → OR < 1: that attribute makes repeat purchase LESS likely.")
print("  → Attributes whose CI (horizontal line) does NOT cross OR=1 are significant.")
print("")
print("FOREST PLOT: Each dot is an odds ratio; the line is the 95% CI.")
print("  → Predictors entirely to the right of OR=1 reliably increase repeat odds.")
print("  → Compare dot positions directly — longer CIs = more uncertainty.")
"""
    })

    # 14. CLV Regression
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.4 OLS Regression: Drivers of Total Customer Value

What variables predict the total monetary value of a customer over time? We regress total historical revenue against behavioural metrics like frequency and average discount, alongside categorical demographics."""
    })

    cells.append({
        "cell_type": "code",
        "source": """if 'customer_type' in customers.columns:
    # ── Build customer-level dataset ──────────────────────────────────────────
    cust_val_df = rfm.merge(df[['customer_id', 'customer_type', 'segment']].drop_duplicates(), on='customer_id', how='left')
    avg_disc = df.groupby('customer_id')['discount_percentage'].mean().reset_index()
    cust_val_df = cust_val_df.merge(avg_disc, on='customer_id', how='left')

    try:
        # ── Original CLV OLS ──────────────────────────────────────────────────
        formula_clv = "monetary ~ frequency + discount_percentage + C(customer_type) + C(segment)"
        model_clv = smf_ols(formula_clv, data=cust_val_df).fit()
        print("═" * 70)
        print("  ORIGINAL CLV OLS — continuous predictors in natural units")
        print("═" * 70)
        print(model_clv.summary())

        # ── Standardised CLV OLS ──────────────────────────────────────────────
        # Z-score continuous predictors: frequency and discount_percentage
        clv_std = cust_val_df.copy()
        cont_clv = ['frequency', 'discount_percentage']
        for v in cont_clv:
            m, s = clv_std[v].mean(), clv_std[v].std()
            clv_std[v] = (clv_std[v] - m) / s
            print(f"  {v}: mean={m:.4f}, SD={s:.4f}  → z-scored")

        model_clv_std = smf_ols(formula_clv, data=clv_std).fit()
        print()
        print("═" * 70)
        print("  STANDARDISED CLV OLS — continuous predictors z-scored")
        print("  β = change in total customer revenue per 1 SD increase in predictor")
        print("═" * 70)
        print(model_clv_std.summary())

        # ── Standardised coefficient plot ─────────────────────────────────────
        coef_clv  = model_clv_std.params.drop('Intercept', errors='ignore')
        err_clv   = model_clv_std.bse.drop('Intercept', errors='ignore')

        labels_clv = [c.replace('C(customer_type)[T.', 'CustType: ').replace(']', '')
                       .replace('C(segment)[T.', 'Segment: ')
                       .replace('discount_percentage', 'Avg Discount (std)')
                       .replace('frequency', 'Frequency (std)')
                      for c in coef_clv.index]

        fig, axes = plt.subplots(1, 2, figsize=(16, max(4, len(coef_clv) * 0.45)))

        # Coefficient plot
        ax = axes[0]
        colors_clv = [COLORS['secondary'] if v < 0 else COLORS['primary'] for v in coef_clv.values]
        ax.barh(labels_clv, coef_clv.values, xerr=1.96 * err_clv.values,
                color=colors_clv, alpha=0.85, edgecolor='white', capsize=4)
        ax.axvline(0, color='#1F2937', linewidth=1.2, linestyle='--')
        ax.set_xlabel('Coefficient (β)')
        ax.set_title('CLV OLS — Standardised Coefficients (blue=positive, red=negative; 95% CI)', pad=10)
        ax.grid(axis='x', linestyle='--', alpha=0.4)

        # Residuals vs Fitted
        axes[1].scatter(model_clv_std.fittedvalues, model_clv_std.resid,
                        alpha=0.5, color=COLORS['primary'], edgecolors='white', s=60)
        axes[1].axhline(0, color=COLORS['secondary'], linewidth=1.5, linestyle='--')
        axes[1].set_xlabel('Fitted values')
        axes[1].set_ylabel('Residuals')
        axes[1].set_title('Residuals vs Fitted (Standardised CLV Model)')
        axes[1].grid(linestyle='--', alpha=0.4)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error in CLV regression: {e}")

print()
print('─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("ORIGINAL CLV OLS: coefficients are in dollars per unit (frequency count, discount %, etc.).")
print("  → Useful for asking: if a customer buys 1 more time, how much more are they worth?")
print("")
print("STANDARDISED CLV OLS: frequency and discount_percentage are z-scored.")
print("  → Their coefficients now answer: which has MORE impact on lifetime value?")
print("  → Frequency (std) vs Avg Discount (std) — the bigger |β|, the stronger driver.")
print("  → Dummies (customer_type, segment) are already 0/1 — not scaled.")
print("")
print("COEFFICIENT PLOT: bars that don't cross zero are statistically significant.")
print("  → Compare bar lengths across ALL predictors to rank their importance.")
print("  → If Frequency (std) >> Discount (std), driving repeat visits matters more")
print("    than optimising discount strategy for increasing customer lifetime value.")
"""
    })

    # 15. ANOVA - Channel/Branch Revenue
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.5 ANOVA: Mean Revenue Across Branches

Are the differences in average revenue across our branches statistically significant, or just random noise? We use a one-way ANOVA test to find out."""
    })

    cells.append({
        "cell_type": "code",
        "source": """import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Group data
branches = df['branch_id'].unique()
data_groups = [df[df['branch_id'] == b]['net_revenue'] for b in branches]

# Perform ANOVA
f_stat, p_val = stats.f_oneway(*data_groups)
print(f"ANOVA F-statistic: {f_stat:.2f}, p-value: {p_val:.4e}")

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x='branch_id', y='net_revenue', palette=COLORS['category_palette'], showfliers=False)
plt.title('Net Revenue Distribution by Branch (Outliers Excluded)', fontsize=14)
plt.xlabel('Branch ID')
plt.ylabel('Net Revenue')
plt.show()

# Tukey HSD if significant
if p_val < 0.05:
    print("ANOVA is significant. Performing Tukey HSD post-hoc test to find which pairs differ:")
    tukey = pairwise_tukeyhsd(endog=df['net_revenue'], groups=df['branch_id'], alpha=0.05)
    print(tukey)

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"The ANOVA test returned a p-value of {p_val:.4e}.")
print("If p < 0.05, we reject the null hypothesis; there is a statistically significant difference in mean revenue between AT LEAST TWO branches.")
print("The boxplot visualizes these differences. If the ANOVA was significant, the Tukey HSD output tells us exactly *which* specific branches are different from each other.")
print("Business Implication: If 'Branch A' significantly outperforms 'Branch B', management must investigate Branch A's practices (staffing, inventory, local marketing) to apply best practices across the network.")
"""
    })

    # 16. Chi-Square - Payment Status vs Customer Type
    cells.append({
        "cell_type": "markdown",
        "source": """## 3.6 Chi-Square Test: Payment Default Risk by Segment

Is late payment associated with specific customer types? We use a Chi-Square test of independence to see if payment status is dependent on customer segmentation."""
    })

    cells.append({
        "cell_type": "code",
        "source": """if 'customer_type' in customers.columns and 'payment_status' in df.columns:
    # Contingency Table
    contingency_table = pd.crosstab(df['customer_type'], df['payment_status'])
    
    # Chi-Square Test
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    
    # Cramér's V for effect size
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    cramer_v = np.sqrt(chi2 / (n * min_dim))
    
    print(f"Chi-Square Statistic: {chi2:.2f}")
    print(f"P-value: {p:.4e}")
    print(f"Cramér's V (Effect Size): {cramer_v:.4f}\\n")
    
    # Plot Observed vs Expected Heatmap
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    
    sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues', ax=ax[0])
    ax[0].set_title('Observed Frequencies', fontsize=14)
    
    sns.heatmap(expected, annot=True, fmt='.1f', cmap='Oranges', ax=ax[1])
    ax[1].set_title('Expected Frequencies (Under Null Hypothesis)', fontsize=14)
    
    plt.tight_layout()
    plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"The Chi-Square test (p={p:.4e}) evaluates if payment status and customer type are independent.")
print("If p < 0.05, they are dependent. Cramér's V measures the strength of this association (0 to 1).")
print("Comparing the Observed vs. Expected heatmaps shows exactly where the deviations occur.")
print("Risk Implications: If 'SME' has a much higher observed 'Overdue' count than expected, credit policies for SMEs need tightening.")
"""
    })

    return cells
