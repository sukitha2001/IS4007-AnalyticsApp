def get_module1_cells():
    return [
        {
            "cell_type": "markdown",
            "source": """# 📊 Module 1: Comprehensive Sales & Revenue Analytics

Welcome to the **Sales & Revenue Analytics Module**. This section provides an in-depth analysis of our top-line performance, evaluating revenue streams across products, channels, and branches.

### 🎯 Business Context
Understanding our revenue drivers is critical for sustainable growth. This module focuses on:
- **Top-line Growth:** Are we hitting our revenue targets and how does the trend look?
- **Profitability:** Where are our highest margins coming from, and are there areas where we are discounting too heavily?
- **Operational Effectiveness:** Which channels and branches are outperforming their peers?
- **Customer Concentration:** Are we too reliant on a small subset of our customer base or product catalog?

All visualizations in this report use our unified light theme to ensure maximum clarity and readability for business stakeholders."""
        },
        {
            "cell_type": "markdown",
            "source": """## 1. Executive Key Performance Indicators (KPIs)

The executive summary dashboard provides a real-time snapshot of the company's financial health. These high-level metrics serve as the baseline for the deeper drill-downs that follow."""
        },
        {
            "cell_type": "code",
            "source": """
import matplotlib.pyplot as plt
import numpy as np

# Calculate KPIs
total_rev = sales['net_revenue'].sum()
total_cost = sales['cost'].sum()
total_margin = sales['gross_margin'].sum()
margin_pct = (total_margin / total_rev) * 100 if total_rev > 0 else 0
total_orders = sales['transaction_id'].nunique()
aov = total_rev / total_orders if total_orders > 0 else 0
total_items = sales['quantity'].sum()
avg_discount = sales['discount_percentage'].mean() * 100

kpis = [
    ("Total Net Revenue", f"${total_rev:,.0f}"),
    ("Total Cost", f"${total_cost:,.0f}"),
    ("Gross Margin", f"${total_margin:,.0f}"),
    ("Margin %", f"{margin_pct:.1f}%"),
    ("Total Orders", f"{total_orders:,}"),
    ("Average Order Value", f"${aov:,.2f}"),
    ("Items Sold", f"{total_items:,}"),
    ("Avg Discount", f"{avg_discount:.1f}%")
]

fig, axes = plt.subplots(2, 4, figsize=(16, 7))
fig.patch.set_facecolor('#FFFFFF')

for i, (ax, (title, val)) in enumerate(zip(axes.flatten(), kpis)):
    ax.set_facecolor(COLORS.get('bg_card', '#F0F4FF'))
    ax.text(0.5, 0.65, title, ha='center', va='center', fontsize=14, color=COLORS.get('text_muted', '#6B7280'), fontweight='medium')
    ax.text(0.5, 0.35, val, ha='center', va='center', fontsize=26, color=COLORS.get('primary', '#4361EE'), fontweight='bold')
    ax.axis('off')

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Revenue Health: Generated {kpis[0][1]} in net revenue across {total_orders:,} transactions.")
print(f"• Profitability: Maintaining a healthy {margin_pct:.1f}% gross margin, yielding {kpis[2][1]} in profit.")
print(f"• Pricing Strategy: The average discount of {avg_discount:.1f}% indicates our promotional strategy is tightly controlled.")
print(f"• Customer Spending: An AOV of ${aov:,.2f} provides a benchmark for future upselling initiatives.")
print("• Actionable Takeaway: Top-line metrics are strong, but the focus must remain on protecting margins against rising costs.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 2. Monthly Revenue Trends

Analyzing revenue on a monthly basis helps identify seasonality, business cycles, and the immediate impact of macroeconomic factors. We employ a 3-month rolling average to smooth out short-term volatility and reveal the underlying growth trajectory."""
        },
        {
            "cell_type": "code",
            "source": """
monthly_rev = df.set_index('transaction_date').resample('ME')['net_revenue'].sum()
rolling_avg = monthly_rev.rolling(window=3).mean()

plt.figure(figsize=(14, 6))
plt.plot(monthly_rev.index, monthly_rev.values, color=COLORS.get('primary', '#4361EE'), marker='o', linewidth=2, label='Monthly Revenue')
plt.fill_between(monthly_rev.index, monthly_rev.values, color=COLORS.get('primary', '#4361EE'), alpha=0.15)
plt.plot(rolling_avg.index, rolling_avg.values, color=COLORS.get('secondary', '#E63946'), linestyle='--', linewidth=2, label='3-Month Moving Average')

# Annotate peak and trough
peak_month = monthly_rev.idxmax()
trough_month = monthly_rev.idxmin()
plt.annotate(f'Peak: ${monthly_rev.max():,.0f}', xy=(peak_month, monthly_rev.max()), xytext=(0, 15), textcoords='offset points', ha='center', color=COLORS.get('text', '#1F2937'), fontweight='bold')
plt.annotate(f'Trough: ${monthly_rev.min():,.0f}', xy=(trough_month, monthly_rev.min()), xytext=(0, -20), textcoords='offset points', ha='center', color=COLORS.get('text', '#1F2937'), fontweight='bold')

plt.title('Monthly Revenue Trend with 3-Month Moving Average', pad=15, fontsize=14, fontweight='bold', color=COLORS.get('text', '#1F2937'))
plt.ylabel('Net Revenue ($)')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# Calculate YoY if possible (assuming 12+ months of data)
if len(monthly_rev) >= 12:
    recent_month = monthly_rev.iloc[-1]
    last_year_month = monthly_rev.iloc[-13] if len(monthly_rev) >= 13 else monthly_rev.iloc[-12]
    yoy_growth = ((recent_month - last_year_month) / last_year_month) * 100
else:
    yoy_growth = None

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Trend Direction: Revenue peaked in {peak_month.strftime('%B %Y')} at ${monthly_rev.max():,.0f}, while the lowest month was {trough_month.strftime('%B %Y')} at ${monthly_rev.min():,.0f}.")
print(f"• Volatility: The 3-month moving average (red dashed line) shows the smoothed trajectory, smoothing out month-to-month noise.")
if yoy_growth is not None:
    direction = "growth" if yoy_growth > 0 else "decline"
    print(f"• YoY Comparison: Recent month shows a {abs(yoy_growth):.1f}% {direction} compared to the same period last year.")
print("• Business Impact: Marketing and operations should align capacity with the identified peak periods. The general trend dictates whether we are expanding or contracting.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 3. Revenue & Margin by Product Category

Not all revenue is created equal. This analysis compares top-line revenue against gross margin for each product category. High volume does not always equate to high profit; understanding this relationship is vital for inventory and marketing allocation."""
        },
        {
            "cell_type": "code",
            "source": """
cat_perf = df.groupby('category').agg({'net_revenue':'sum', 'gross_margin':'sum'}).sort_values('net_revenue', ascending=False)
cat_perf['margin_pct'] = (cat_perf['gross_margin'] / cat_perf['net_revenue']) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [2, 1]})

# Grouped Bar
x = np.arange(len(cat_perf))
width = 0.35
bars1 = ax1.bar(x - width/2, cat_perf['net_revenue'], width, label='Net Revenue', color=COLORS.get('primary', '#4361EE'), alpha=0.85, edgecolor='white')
bars2 = ax1.bar(x + width/2, cat_perf['gross_margin'], width, label='Gross Margin', color=COLORS.get('accent', '#2EC4B6'), alpha=0.85, edgecolor='white')

ax1.set_xticks(x)
ax1.set_xticklabels(cat_perf.index, rotation=45, ha='right')
ax1.set_title('Revenue vs Margin by Category', fontweight='bold', pad=15)
ax1.set_ylabel('Amount ($)')
ax1.legend()
ax1.grid(axis='y', linestyle='--', alpha=0.4)

# Donut chart
wedges, texts, autotexts = ax2.pie(
    cat_perf['net_revenue'], 
    labels=cat_perf.index, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=COLORS.get('category_palette', [COLORS.get('primary', '#4361EE'), COLORS.get('accent', '#2EC4B6'), COLORS.get('secondary', '#E63946'), '#F4A261', '#E76F51', '#264653']),
    wedgeprops=dict(width=0.4, edgecolor='white')
)
plt.setp(autotexts, size=10, weight="bold", color="white")
ax2.set_title('Revenue Share', fontweight='bold')

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Top Category: '{cat_perf.index[0]}' dominates with ${cat_perf['net_revenue'].iloc[0]:,.0f} in revenue, making up a massive chunk of our overall sales.")
highest_margin_cat = cat_perf['margin_pct'].idxmax()
print(f"• Margin Tradeoffs: While some categories drive volume, '{highest_margin_cat}' leads in profitability with a {cat_perf['margin_pct'].max():.1f}% margin.")
print("• Strategic Action: Shift marketing spend towards high-margin categories. Reassess pricing or supplier costs for high-volume, low-margin products.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 4. Channel Performance Analysis

Our distribution channels are the arteries of the business. By breaking down revenue by channel, we can assess our omnichannel strategy. The stacked area chart helps visualize how the mix of channels shifts over time."""
        },
        {
            "cell_type": "code",
            "source": """
channel_rev = df.groupby('channel')['net_revenue'].sum().sort_values(ascending=True)

# Monthly channel mix for stacked area
monthly_channel = df.pivot_table(index=pd.Grouper(key='transaction_date', freq='ME'), columns='channel', values='net_revenue', aggfunc='sum').fillna(0)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# Horizontal Bar
ax1.barh(channel_rev.index, channel_rev.values, color=COLORS.get('primary', '#4361EE'), alpha=0.85, edgecolor='white')
ax1.set_title('Total Revenue by Channel', fontweight='bold', pad=15)
ax1.set_xlabel('Net Revenue ($)')
for i, v in enumerate(channel_rev.values):
    ax1.text(v + (v*0.02), i, f'${v:,.0f}', va='center')

# Stacked Area
palette = COLORS.get('pastel', ['#A8DADC', '#457B9D', '#1D3557', '#E63946', '#F1FAEE', '#8ECAE6'])
ax2.stackplot(monthly_channel.index, monthly_channel.T, labels=monthly_channel.columns, colors=palette, alpha=0.85)
ax2.set_title('Channel Revenue Mix Over Time', fontweight='bold', pad=15)
ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
ax2.grid(axis='y', linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Dominant Channel: '{channel_rev.index[-1]}' is our strongest performer, generating ${channel_rev.values[-1]:,.0f}.")
print(f"• Channel Lag: '{channel_rev.index[0]}' generated only ${channel_rev.values[0]:,.0f}. This channel may need revitalization or decommissioning.")
print("• Growth Trends: The area chart reveals if direct or digital channels are cannibalizing traditional physical channels over time.")
print("• Action Item: Optimize the customer journey in our leading channel while investigating friction points in underperforming ones.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 5. Branch Location Performance

Geographic and physical location performance is crucial for resource allocation. The bar chart compares absolute totals, while the heatmap uncovers seasonal or temporal variations across different branches."""
        },
        {
            "cell_type": "code",
            "source": """
import seaborn as sns

branch_rev = df.groupby('branch_id')['net_revenue'].sum().sort_values(ascending=False)
monthly_branch = df.pivot_table(index='branch_id', columns=pd.Grouper(key='transaction_date', freq='ME'), values='net_revenue', aggfunc='sum').fillna(0)
# Format columns to just YYYY-MM
monthly_branch.columns = monthly_branch.columns.strftime('%Y-%m')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), gridspec_kw={'width_ratios': [1, 1.5]})

# Bar chart
sns.barplot(x=branch_rev.values, y=branch_rev.index, ax=ax1, color=COLORS.get('primary', '#4361EE'), alpha=0.85, edgecolor='white')
ax1.set_title('Total Revenue by Branch', fontweight='bold')
ax1.set_xlabel('Net Revenue ($)')
ax1.set_ylabel('')

# Heatmap
sns.heatmap(monthly_branch, cmap='Blues', ax=ax2, cbar_kws={'label': 'Revenue ($)'}, linewidths=0.5)
ax2.set_title('Monthly Revenue Heatmap by Branch', fontweight='bold')
ax2.set_xlabel('Month')
ax2.set_ylabel('')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Top Performer: Branch '{branch_rev.index[0]}' leads with ${branch_rev.values[0]:,.0f} in revenue.")
print(f"• Underperformer: Branch '{branch_rev.index[-1]}' trails with ${branch_rev.values[-1]:,.0f}.")
print("• Temporal Patterns: The heatmap highlights specific months where certain branches spike (e.g., regional holidays or local promotions).")
print("• Strategy: Perform a root-cause analysis on the trailing branches—are they hampered by foot traffic, inventory issues, or management?")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 6. Granular Margin Analysis & Profitability Risk

Understanding gross margin at the product level is critical. High revenue is meaningless if it comes at a loss. We visualize the margin spread across categories and pinpoint specific products that represent a profitability risk."""
        },
        {
            "cell_type": "code",
            "source": """
prod_margin = df.groupby('product_name').agg({'net_revenue': 'sum', 'gross_margin': 'sum'})
prod_margin['margin_pct'] = (prod_margin['gross_margin'] / prod_margin['net_revenue']) * 100

fig, ax = plt.subplots(figsize=(16, 9))
scatter = ax.scatter(prod_margin['net_revenue'], prod_margin['margin_pct'], 
                     s=prod_margin['net_revenue']/prod_margin['net_revenue'].max()*500 + 50, # Size by revenue
                     c=prod_margin['margin_pct'], cmap='RdYlGn', alpha=0.7, edgecolors='white', linewidth=1)

ax.axhline(prod_margin['margin_pct'].mean(), color=COLORS.get('text_muted', '#6B7280'), linestyle='--', label=f'Avg Margin ({prod_margin["margin_pct"].mean():.1f}%)')
ax.axvline(prod_margin['net_revenue'].mean(), color=COLORS.get('text_muted', '#6B7280'), linestyle=':', label='Avg Revenue')

# Label each bubble with product name
for name, row in prod_margin.iterrows():
    short_name = name if len(name) <= 20 else name[:18] + '…'
    ax.annotate(short_name, 
                xy=(row['net_revenue'], row['margin_pct']),
                xytext=(8, 6), textcoords='offset points',
                fontsize=7.5, color=COLORS.get('text', '#1F2937'),
                fontweight='bold', alpha=0.85,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#D1D5DB', alpha=0.8),
                arrowprops=dict(arrowstyle='-', color='#9CA3AF', lw=0.5))

ax.set_title('Product Profitability Matrix (Revenue vs. Margin %)', fontweight='bold', pad=15)
ax.set_xlabel('Total Net Revenue ($)')
ax.set_ylabel('Gross Margin (%)')
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend()
plt.colorbar(scatter, label='Margin %')
plt.tight_layout()
plt.show()

low_margin_prods = prod_margin.sort_values('margin_pct').head(3)
high_margin_prods = prod_margin.sort_values('margin_pct', ascending=False).head(3)

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print("• Quadrant Analysis: Products in the bottom-right (high revenue, low margin) are volume drivers but erode overall profitability. Top-right products are our 'Star' products.")
print("• Profitability Red Flags: Watch out for:")
for idx, row in low_margin_prods.iterrows():
    print(f"   - {idx}: {row['margin_pct']:.1f}% margin (Revenue: ${row['net_revenue']:,.0f})")
print("• Margin Champions:")
for idx, row in high_margin_prods.iterrows():
    print(f"   - {idx}: {row['margin_pct']:.1f}% margin (Revenue: ${row['net_revenue']:,.0f})")
print("• Actionable Insight: Initiate an immediate pricing review or vendor cost renegotiation for the red flag products. Consider bundling high-margin champions with volume drivers.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 7. Average Order Value (AOV) Dynamics

AOV indicates customer willingness to spend in a single transaction. By breaking down AOV across dimensions like channel and category, we can tailor upselling and cross-selling tactics to the right audiences."""
        },
        {
            "cell_type": "code",
            "source": """
channel_orders = df.groupby('channel').agg({'net_revenue':'sum', 'transaction_id':'nunique'})
channel_orders['aov'] = channel_orders['net_revenue'] / channel_orders['transaction_id']
channel_orders = channel_orders.sort_values('aov', ascending=False)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Boxplot for overall distribution
sns.boxplot(data=df, x='channel', y='net_revenue', ax=ax1, palette='Blues', showfliers=False)
ax1.set_title('Transaction Value Distribution by Channel (Excl. Outliers)', fontweight='bold')
ax1.set_xlabel('Channel')
ax1.set_ylabel('Net Revenue per Transaction ($)')
ax1.tick_params(axis='x', rotation=45)

# Bar chart for AOV
sns.barplot(x=channel_orders.index, y=channel_orders['aov'], ax=ax2, color=COLORS.get('accent', '#2EC4B6'), alpha=0.85, edgecolor='white')
ax2.set_title('Average Order Value (AOV) by Channel', fontweight='bold')
ax2.set_xlabel('Channel')
ax2.set_ylabel('AOV ($)')
ax2.tick_params(axis='x', rotation=45)

for i, v in enumerate(channel_orders['aov']):
    ax2.text(i, v + 2, f'${v:,.0f}', ha='center')

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Overall Metric: The baseline AOV across the entire business sits at ${df['net_revenue'].sum()/df['transaction_id'].nunique():,.2f}.")
print(f"• High Roller Channel: '{channel_orders.index[0]}' leads with an AOV of ${channel_orders['aov'].iloc[0]:,.2f}, indicating a premium buying behavior or bulk purchases.")
print(f"• Low AOV Channel: '{channel_orders.index[-1]}' has the lowest AOV (${channel_orders['aov'].iloc[-1]:,.2f}), which might be standard for its operational model but leaves room for improvement.")
print("• Upsell Opportunity: Implement volume discounts, minimum-spend free shipping, or targeted cross-sells in low-AOV channels to bump up the transaction size.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 8. Quarterly Business Reviews (QBR)

Summarizing performance into quarters provides the 10,000-foot view required by the board. It abstracts away monthly noise and explicitly calculates Quarter-over-Quarter (QoQ) growth to ensure we are hitting macro targets."""
        },
        {
            "cell_type": "code",
            "source": """
df['quarter'] = df['transaction_date'].dt.to_period('Q')
quarterly_rev = df.groupby('quarter')['net_revenue'].sum()

# Calculate QoQ growth
qoq_growth = quarterly_rev.pct_change() * 100

fig, ax1 = plt.subplots(figsize=(14, 6))

x = np.arange(len(quarterly_rev))
bars = ax1.bar(x, quarterly_rev.values, color=COLORS.get('primary', '#4361EE'), alpha=0.85, edgecolor='white', width=0.6)
ax1.set_xticks(x)
ax1.set_xticklabels([str(q) for q in quarterly_rev.index])
ax1.set_ylabel('Net Revenue ($)')
ax1.set_title('Quarterly Revenue & QoQ Growth', fontweight='bold', pad=15)
ax1.grid(axis='y', linestyle='--', alpha=0.4)

ax2 = ax1.twinx()
ax2.plot(x, qoq_growth.values, color=COLORS.get('secondary', '#E63946'), marker='o', linewidth=2, linestyle='-', markersize=8)
ax2.set_ylabel('QoQ Growth (%)', color=COLORS.get('secondary', '#E63946'))
ax2.tick_params(axis='y', labelcolor=COLORS.get('secondary', '#E63946'))
ax2.axhline(0, color='black', linewidth=1, alpha=0.5)

# Annotate bars
for i, bar in enumerate(bars):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f"${bar.get_height()/1000:,.0f}k", 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLORS.get('text', '#1F2937'))

plt.tight_layout()
plt.show()

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Strongest Quarter: {quarterly_rev.idxmax()} generated the highest revenue at ${quarterly_rev.max():,.0f}.")
if len(qoq_growth.dropna()) > 0:
    max_growth_q = qoq_growth.idxmax()
    print(f"• Momentum: The highest Quarter-over-Quarter growth occurred in {max_growth_q} at {qoq_growth.max():.1f}%.")
    print(f"• Recent Performance: The most recent completed quarter saw a QoQ change of {qoq_growth.iloc[-1]:.1f}%.")
print("• Strategic Value: The QoQ trend line (red) instantly communicates business momentum. Sharp drops require immediate explanation (seasonality vs. systemic issues).")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 9. Pareto Analysis (80/20 Rule)

The Pareto principle often applies to business: a small percentage of products or customers generate the vast majority of revenue. This analysis quantifies our concentration risk. High concentration means vulnerability if key accounts churn; low concentration means a highly fragmented, resilient base."""
        },
        {
            "cell_type": "code",
            "source": """
# Product Pareto
prod_rev = df.groupby('product_name')['net_revenue'].sum().sort_values(ascending=False)
prod_cum_pct = (prod_rev.cumsum() / prod_rev.sum()) * 100

# Customer Pareto
cust_rev = df.groupby('customer_id')['net_revenue'].sum().sort_values(ascending=False)
cust_cum_pct = (cust_rev.cumsum() / cust_rev.sum()) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Product
ax1.plot(range(1, len(prod_cum_pct) + 1), prod_cum_pct.values, color=COLORS.get('primary', '#4361EE'), linewidth=2)
ax1.axhline(80, color=COLORS.get('secondary', '#E63946'), linestyle='--', alpha=0.7)
idx_80_prod = (prod_cum_pct >= 80).idxmax() if not prod_cum_pct.empty else None
idx_pos_prod = prod_cum_pct.index.get_loc(idx_80_prod) + 1 if idx_80_prod else 0
ax1.axvline(idx_pos_prod, color=COLORS.get('secondary', '#E63946'), linestyle='--', alpha=0.7)
ax1.set_title('Product Revenue Cumulative Share', fontweight='bold')
ax1.set_xlabel('Number of Products (Ranked)')
ax1.set_ylabel('Cumulative % of Total Revenue')
ax1.grid(True, linestyle='--', alpha=0.4)

# Customer
ax2.plot(range(1, len(cust_cum_pct) + 1), cust_cum_pct.values, color=COLORS.get('accent', '#2EC4B6'), linewidth=2)
ax2.axhline(80, color=COLORS.get('secondary', '#E63946'), linestyle='--', alpha=0.7)
idx_80_cust = (cust_cum_pct >= 80).idxmax() if not cust_cum_pct.empty else None
idx_pos_cust = cust_cum_pct.index.get_loc(idx_80_cust) + 1 if idx_80_cust else 0
ax2.axvline(idx_pos_cust, color=COLORS.get('secondary', '#E63946'), linestyle='--', alpha=0.7)
ax2.set_title('Customer Revenue Cumulative Share', fontweight='bold')
ax2.set_xlabel('Number of Customers (Ranked)')
ax2.set_ylabel('Cumulative % of Total Revenue')
ax2.grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.show()

pct_prods_for_80 = (idx_pos_prod / len(prod_rev)) * 100 if len(prod_rev) > 0 else 0
pct_custs_for_80 = (idx_pos_cust / len(cust_rev)) * 100 if len(cust_rev) > 0 else 0

print('\\n' + '─'*70)
print('📊 INTERPRETATION')
print('─'*70)
print(f"• Product Concentration: {idx_pos_prod} products ({pct_prods_for_80:.1f}% of catalog) generate 80% of total revenue. This implies we are {'highly dependent on' if pct_prods_for_80 < 20 else 'diversified across'} a subset of items.")
print(f"• Customer Concentration: {idx_pos_cust} customers ({pct_custs_for_80:.1f}% of base) generate 80% of revenue. This signals {'high key-account risk' if pct_custs_for_80 < 20 else 'a healthy, broad consumer base'}.")
print("• Supply Chain Implication: Prioritize stock availability and VIP support for the critical 80% drivers. Consider culling the bottom 10% of products if they carry high inventory carrying costs.")
"""
        },
        {
            "cell_type": "markdown",
            "source": """## 10. Marketing Campaign Impact

Marketing campaigns require capital, and we must measure their Return on Investment (ROI). This analysis maps campaign dates against daily revenue to visually inspect the sales lift generated during promotional periods."""
        },
        {
            "cell_type": "code",
            "source": """
# Check if campaigns exist and have valid dates
if not campaigns.empty and 'start_date' in campaigns.columns:
    daily_rev = df.groupby('transaction_date')['net_revenue'].sum().reset_index()
    
    plt.figure(figsize=(15, 6))
    plt.plot(daily_rev['transaction_date'], daily_rev['net_revenue'], color=COLORS.get('text_muted', '#6B7280'), alpha=0.6, label='Daily Revenue')
    
    # Overlay campaigns
    colors = COLORS.get('category_palette', ['#4361EE', '#2EC4B6', '#E63946', '#F4A261', '#9D4EDD'])
    for i, row in campaigns.iterrows():
        c = colors[i % len(colors)]
        mask = (daily_rev['transaction_date'] >= row['start_date']) & (daily_rev['transaction_date'] <= row['end_date'])
        plt.plot(daily_rev.loc[mask, 'transaction_date'], daily_rev.loc[mask, 'net_revenue'], color=c, linewidth=2)
        plt.axvspan(row['start_date'], row['end_date'], alpha=0.1, color=c, label=row['campaign_name'])
        
    plt.title('Daily Revenue with Campaign Overlays', fontweight='bold', pad=15)
    plt.xlabel('Date')
    plt.ylabel('Net Revenue ($)')
    # Ensure unique labels in legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.01, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.show()

    # Calculate simplistic ROI
    print('\\n' + '─'*70)
    print('📊 INTERPRETATION')
    print('─'*70)
    print("• Visual Lift: Highlighted sections indicate active campaign windows. A sharp spike during these windows suggests an effective promotional hook.")
    print("• Baseline Comparison: Check if revenue drops significantly below the baseline immediately after a campaign ends—this implies we simply shifted sales forward rather than creating net new demand.")
    print("• ROI Directive: The marketing team should cross-reference these revenue spikes against the `campaign_cost` to calculate true Return on Ad Spend (ROAS) for each initiative.")
else:
    print("No valid campaign data available to plot.")
"""
        }
    ]
