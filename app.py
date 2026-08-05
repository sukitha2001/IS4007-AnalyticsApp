import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_loader import load_data
from utils.theme import apply_theme

# Import the views
import importlib
import views.customer_analytics
import views.product_and_channel
import views.pricing_and_discount
import views.leakage_and_underperformance
import views.recommendations
importlib.reload(views.customer_analytics)
importlib.reload(views.product_and_channel)
importlib.reload(views.pricing_and_discount)
importlib.reload(views.leakage_and_underperformance)
importlib.reload(views.recommendations)
from views.customer_analytics import render_customer_analytics
from views.product_and_channel import render_product_and_channel
from views.pricing_and_discount import render_pricing_and_discount
from views.revenue_forecasting import render_revenue_forecasting
from views.leakage_and_underperformance import render_leakage_and_underperformance
from views.recommendations import render_recommendations

# Force reload

st.set_page_config(page_title="Analytics Command Center", page_icon="⚡", layout="wide")
apply_theme()

# The Animated Top Navigation Bar
st.markdown("<br>", unsafe_allow_html=True)
pages = [
    "Executive Revenue Analytics", 
    "Customer Analytics", 
    "Product & Channel", 
    "Pricing & Discount", 
    "Revenue Forecasting", 
    "Leakage & Underperformance", 
    "Recommendations"
]

# Top navigation using segmented control
selection = st.segmented_control(
    label="Navigation",
    options=pages,
    default="Executive Revenue Analytics",
    key="main_nav",
    label_visibility="collapsed",
)

st.markdown("<hr style='margin-top: 0; margin-bottom: 2rem; border-color: rgba(128,128,128,0.2);'>", unsafe_allow_html=True)

# Main Routing Logic
if selection == "Executive Revenue Analytics":
    col_header1, col_header2 = st.columns([1, 1])
    with col_header1:
        st.markdown("<h1 style='margin-bottom: 0;' class='text-gradient'>Executive Revenue Analytics</h1>", unsafe_allow_html=True)
    with col_header2:
        st.write("")

    sales, customers, products, campaigns = load_data()
    if sales.empty:
        st.warning("Data could not be loaded. Please ensure the generated_data directory exists.")
    else:
        # --- GLOBAL FILTERS ---
        st.markdown("<h3 style='color: gray; font-size: 14px; text-transform: uppercase; margin-bottom: 0px;'>Dashboard Filters</h3>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3 = st.columns(3)
        
        min_date = sales['transaction_date'].min().date()
        max_date = sales['transaction_date'].max().date()
        with f_col1:
            date_range = st.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
        
        channels = sales['channel'].unique().tolist()
        with f_col2:
            selected_channels = st.multiselect("Sales Channel", options=channels, default=channels)
            
        categories = products['category'].unique().tolist()
        with f_col3:
            selected_categories = st.multiselect("Product Category", options=categories, default=categories)
            
        filtered_sales = sales.copy()
        if len(date_range) == 2:
            filtered_sales = filtered_sales[(filtered_sales['transaction_date'].dt.date >= date_range[0]) & 
                                            (filtered_sales['transaction_date'].dt.date <= date_range[1])]
        if selected_channels:
            filtered_sales = filtered_sales[filtered_sales['channel'].isin(selected_channels)]
        if selected_categories:
            valid_products = products[products['category'].isin(selected_categories)]['product_id']
            filtered_sales = filtered_sales[filtered_sales['product_id'].isin(valid_products)]

        st.write("") # Spacing after filters

        tabs = st.segmented_control(
            label="View",
            options=['Overview', 'Analytics', 'Reports'],
            default='Overview',
            key="main_tabs",
            label_visibility="collapsed",
        )

        if filtered_sales.empty:
            st.warning("No data available for the selected filters.")
        elif tabs == 'Overview':
            # 4 metric cards
            total_revenue = filtered_sales['net_revenue'].sum()
            unique_customers = filtered_sales['customer_id'].nunique()
            total_sales = len(filtered_sales)
        
            # Calculate active in the last 30 days
            last_date = filtered_sales['transaction_date'].max()
            if pd.notna(last_date):
                active_now = len(filtered_sales[filtered_sales['transaction_date'] >= (last_date - pd.Timedelta(days=30))]['customer_id'].unique())
            else:
                active_now = 0
            kpi_cards = [
                {"icon": "💰", "label": "Total Revenue",  "value": f"${total_revenue:,.0f}", "desc": "Lifetime net revenue",          "color": "#3b82f6"},
                {"icon": "👥", "label": "Customers",       "value": f"{unique_customers:,}",  "desc": "Unique buyers",                "color": "#8b5cf6"},
                {"icon": "🛒", "label": "Total Sales",     "value": f"{total_sales:,}",        "desc": "Total transactions",           "color": "#10b981"},
                {"icon": "⚡", "label": "Active (30d)",    "value": f"{active_now:,}",         "desc": "Customers active recently",    "color": "#f59e0b"},
            ]
            kpi_cols = st.columns(4)
            for col, card in zip(kpi_cols, kpi_cards):
                with col:
                    st.html(f"""
                    <div style="
                        background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
                        border: 1px solid rgba(255,255,255,0.08);
                        border-top: 2px solid {card['color']};
                        border-radius: 12px;
                        padding: 1.4rem 1.5rem 1.2rem;
                        position: relative;
                        overflow: hidden;
                        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
                    ">
                        <div style="
                            position: absolute; top: -20px; right: -10px;
                            font-size: 5rem; opacity: 0.06; user-select: none;
                        ">{card['icon']}</div>
                        <p style="margin:0 0 0.5rem; font-size:0.75rem; font-weight:600;
                                  text-transform:uppercase; letter-spacing:0.08em;
                                  color:{card['color']};">{card['label']}</p>
                        <p style="margin:0 0 0.4rem; font-size:2rem; font-weight:800;
                                  color:#f1f5f9; line-height:1.1;">{card['value']}</p>
                        <p style="margin:0; font-size:0.78rem; color:#64748b;">{card['desc']}</p>
                    </div>
                    """)

            st.write("")  # spacing
            st.write("")

            # Prepare Data for new charts
            # True time-series using month-end dates for continuous x-axis
            monthly = filtered_sales.resample('ME', on='transaction_date')['net_revenue'].sum().reset_index()
            monthly['3M_MA'] = monthly['net_revenue'].rolling(window=3).mean()
        
            sales_prod = filtered_sales.merge(products, on='product_id', how='left')
            category_rev = sales_prod.groupby('category')['net_revenue'].sum().reset_index()
        
            category_margin = products.groupby('category')['margin_percentage'].mean().reset_index()
            cat_rev_margin = category_rev.merge(category_margin, on='category')
        
            filtered_sales['quarter'] = filtered_sales['transaction_date'].dt.to_period('Q').astype(str)
            quarterly = filtered_sales.groupby('quarter')['net_revenue'].sum().reset_index()
            quarterly['QoQ_Growth'] = quarterly['net_revenue'].pct_change() * 100

            # ROW 2
            row2_col1, row2_col2 = st.columns([2.5, 1.5])
            with row2_col1:
                st.markdown("<h2 class='text-gradient'>Revenue Trend (3M MA)</h2>", unsafe_allow_html=True)
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(x=monthly['transaction_date'], y=monthly['net_revenue'], name='Revenue', 
                                          mode='lines', fill='tozeroy', line=dict(color='#3b82f6', width=2), 
                                          fillcolor='rgba(59, 130, 246, 0.2)'))
                fig1.add_trace(go.Scatter(x=monthly['transaction_date'], y=monthly['3M_MA'], name='3M Moving Avg', line=dict(color='#f59e0b', width=3)))
                fig1.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   xaxis=dict(showgrid=False, tickfont=dict(color="gray")),
                                   yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="gray")),
                                   height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
            
            with row2_col2:
                st.markdown("<h2 class='text-gradient'>Category Share</h2>", unsafe_allow_html=True)
                fig2 = go.Figure(data=[go.Pie(labels=category_rev['category'], values=category_rev['net_revenue'], hole=0.65,
                                              marker=dict(colors=['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899']))])
                fig2.update_layout(margin=dict(t=20, b=20, l=20, r=20), paper_bgcolor="rgba(0,0,0,0)",
                                   height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
                st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

            st.write("")
            st.write("")

            # ROW 3
            row3_col1, row3_col2 = st.columns([2.5, 1.5])
            with row3_col1:
                st.markdown("<h2 class='text-gradient'>Quarterly Growth</h2>", unsafe_allow_html=True)
                from plotly.subplots import make_subplots
                fig3 = make_subplots(specs=[[{"secondary_y": True}]])
                fig3.add_trace(go.Bar(x=quarterly['quarter'], y=quarterly['net_revenue'], name="Revenue", marker_color="#8b5cf6", opacity=0.8), secondary_y=False)
                fig3.add_trace(go.Scatter(x=quarterly['quarter'], y=quarterly['QoQ_Growth'], name="QoQ Growth %", line=dict(color="#10b981", width=4), mode='lines+markers'), secondary_y=True)
                fig3.update_layout(margin=dict(l=0, r=0, t=20, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                fig3.update_xaxes(showgrid=False, tickfont=dict(color="gray"))
                fig3.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="gray"), secondary_y=False)
                fig3.update_yaxes(showgrid=False, tickfont=dict(color="gray"), secondary_y=True)
                st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
            
            with row3_col2:
                st.markdown("<h2 class='text-gradient'>Recent Sales</h2>", unsafe_allow_html=True)
            
                recent_month = filtered_sales['transaction_date'].dt.to_period('M').max()
                current_month_sales = len(filtered_sales[filtered_sales['transaction_date'].dt.to_period('M') == recent_month])
            
                st.markdown(f"<p style='color: gray; font-size: 16px; margin-top: -10px; "
                            f"margin-bottom: 24px;'>You made {current_month_sales} sales this month.</p>",
                            unsafe_allow_html=True)

                recent = filtered_sales.sort_values('transaction_date', ascending=False).head(5)
                recent = recent.merge(customers, on='customer_id', how='left')

                list_html = "<ul class='recent-sales-list'>"
                for _, row in recent.iterrows():
                    name = f"Customer {str(row['customer_id']).split('-')[-1]}"
                    email = f"{name.lower().replace(' ', '.')}@example.com"
                    initials = name[:2].upper()
                    amount = f"+${row['net_revenue']:,.2f}"
                    list_html += f"""<li class='recent-sales-item'>
<div class='rs-avatar'>{initials}</div>
<div class='rs-details'>
<p class='rs-name'>{name}</p>
<p class='rs-email'>{email}</p>
</div>
<div class='rs-amount'>{amount}</div>
</li>"""
                list_html += "</ul>"
                st.markdown(list_html, unsafe_allow_html=True)

            st.write("")
            st.write("")
        
            # ROW 4
            st.markdown("<h2 class='text-gradient'>Revenue vs Margin by Category</h2>", unsafe_allow_html=True)
        
            # Calculate absolute profit and cost for the stacked bar chart
            cat_rev_margin['profit'] = cat_rev_margin['net_revenue'] * (cat_rev_margin['margin_percentage'] / 100)
            cat_rev_margin['cost'] = cat_rev_margin['net_revenue'] - cat_rev_margin['profit']
            cat_rev_margin = cat_rev_margin.sort_values('net_revenue', ascending=False)
        
            fig4 = go.Figure()
            fig4.add_trace(go.Bar(x=cat_rev_margin['category'], y=cat_rev_margin['profit'], name='Profit (Margin)', marker_color='#10b981')) # Emerald
            fig4.add_trace(go.Bar(x=cat_rev_margin['category'], y=cat_rev_margin['cost'], name='Cost', marker_color='#3b82f6')) # Blue
            fig4.update_layout(barmode='stack', margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               height=400, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                               xaxis=dict(showgrid=False, tickfont=dict(color="gray")),
                               yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="gray")))
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
            
        elif tabs == 'Analytics':
            st.markdown("<h2 class='text-gradient'>Daily Revenue & Campaigns</h2>", unsafe_allow_html=True)
            
            # Prepare daily revenue
            daily_rev = filtered_sales.groupby(filtered_sales['transaction_date'].dt.date)['net_revenue'].sum().reset_index()
            daily_rev['transaction_date'] = pd.to_datetime(daily_rev['transaction_date'])
            
            # Ensure dates match for filtering
            start = pd.to_datetime(date_range[0])
            end = pd.to_datetime(date_range[1])
            active_campaigns = campaigns[(pd.to_datetime(campaigns['start_date']) <= end) & 
                                         (pd.to_datetime(campaigns['end_date']) >= start)]
            
            fig_camp = go.Figure()
            fig_camp.add_trace(go.Scatter(x=daily_rev['transaction_date'], y=daily_rev['net_revenue'], name='Daily Revenue',
                                          mode='lines', line=dict(color='#3b82f6', width=2), fill='tozeroy', fillcolor='rgba(59, 130, 246, 0.2)'))
            
            # Add campaign overlays
            colors = ['rgba(236, 72, 153, 0.3)', 'rgba(16, 185, 129, 0.3)', 'rgba(245, 158, 11, 0.3)', 'rgba(139, 92, 246, 0.3)', 'rgba(6, 182, 212, 0.3)']
            for i, (_, camp) in enumerate(active_campaigns.iterrows()):
                c_start = pd.to_datetime(camp['start_date'])
                c_end = pd.to_datetime(camp['end_date'])
                color = colors[i % len(colors)]
                
                fig_camp.add_vrect(x0=c_start, x1=c_end, fillcolor=color, opacity=1, layer="below", line_width=0, 
                                   annotation_text=camp['campaign_name'], annotation_position="top left", annotation_font=dict(color="white"))
                
            fig_camp.update_layout(margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   height=400, xaxis=dict(showgrid=False, tickfont=dict(color="gray")),
                                   yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="gray")))
            st.plotly_chart(fig_camp, use_container_width=True, config={'displayModeBar': False})
            
            st.write("")
            st.write("")
            
            st.markdown("<h2 class='text-gradient'>Product Profitability Matrix</h2>", unsafe_allow_html=True)
            # Scatter plot for products (not categories)
            sales_prod = filtered_sales.merge(products, on='product_id', how='left')
            prod_metrics = sales_prod.groupby(['product_name', 'category', 'margin_percentage'])['net_revenue'].sum().reset_index()
            
            fig_matrix = px.scatter(prod_metrics, x='net_revenue', y='margin_percentage', color='category', 
                                    hover_name='product_name', size='net_revenue', size_max=40,
                                    color_discrete_sequence=['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#ec4899', '#06b6d4'])
                                    
            avg_rev = prod_metrics['net_revenue'].mean()
            avg_margin = prod_metrics['margin_percentage'].mean()
            
            # Add quadrant lines
            fig_matrix.add_hline(y=avg_margin, line_dash="dash", line_color="gray", opacity=0.5)
            fig_matrix.add_vline(x=avg_rev, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Quadrant labels
            fig_matrix.add_annotation(x=prod_metrics['net_revenue'].max(), y=prod_metrics['margin_percentage'].max(), text="Star Products", showarrow=False, font=dict(color="white", size=14), xanchor="right", yanchor="top")
            fig_matrix.add_annotation(x=prod_metrics['net_revenue'].max(), y=prod_metrics['margin_percentage'].min(), text="Cash Cows", showarrow=False, font=dict(color="white", size=14), xanchor="right", yanchor="bottom")
            fig_matrix.add_annotation(x=0, y=prod_metrics['margin_percentage'].max(), text="High Potential", showarrow=False, font=dict(color="white", size=14), xanchor="left", yanchor="top")
            fig_matrix.add_annotation(x=0, y=prod_metrics['margin_percentage'].min(), text="Underperformers", showarrow=False, font=dict(color="white", size=14), xanchor="left", yanchor="bottom")
            
            fig_matrix.update_layout(margin=dict(l=0, r=0, t=30, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                     height=500, xaxis_title="Total Net Revenue ($)", yaxis_title="Gross Margin (%)",
                                     xaxis=dict(showgrid=False, tickfont=dict(color="gray")),
                                     yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="gray")))
            st.plotly_chart(fig_matrix, use_container_width=True, config={'displayModeBar': False})
            
        elif tabs == 'Reports':
            st.markdown("<h2 class='text-gradient' style='margin-bottom: 2rem;'>Executive Summary Report</h2>", unsafe_allow_html=True)
            
            st.html("""
<div style='display: flex; flex-direction: column; gap: 1.5rem;'>
    
    <div style='background-color: rgba(255,255,255,0.03); padding: 1.5rem; border-left: 4px solid #3b82f6; border-radius: 4px;'>
        <h3 style='color: #e2e8f0; font-size: 18px; margin-top: 0;'>Performance Overview</h3>
        <p style='color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 0;'>
            Over the 24-month period (Jan 2023–Dec 2024), the business generated <strong style='color: #fff;'>$5.34 million</strong> in net revenue across <strong style='color: #fff;'>12,922 transactions</strong>. 
            While the business maintained a healthy transaction volume, it experienced a <strong style='color: #ef4444;'>7.5% year-over-year revenue decline</strong> in 2024. 
            Revenue peaks occurred consistently in March/April and November/December, indicating significant sensitivity to holiday and end-of-quarter purchasing behaviour.
        </p>
    </div>

    <div style='background-color: rgba(255,255,255,0.03); padding: 1.5rem; border-left: 4px solid #8b5cf6; border-radius: 4px;'>
        <h3 style='color: #e2e8f0; font-size: 18px; margin-top: 0;'>Product & Channel Breakdown</h3>
        <p style='color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 0;'>
            <strong>Home & Living, Electronics, and Apparel</strong> are the top contributors, accounting for <strong style='color: #fff;'>58.8%</strong> of total revenue. 
            Products such as "Beauty Performance 16" generate net losses due to excessive discounting and require price optimization. 
            <strong style='color: #fff;'>Online sales</strong> dominate at 34.2% of total revenue, with Electronics sold through the Online channel being the single largest revenue-generating combination. 
            Although BR-North is the strongest-performing branch and BR-Central generates 44% less revenue than the top branch, statistical tests indicate that these performance differences are not statistically significant.
        </p>
    </div>

    <div style='background-color: rgba(255,255,255,0.03); padding: 1.5rem; border-left: 4px solid #10b981; border-radius: 4px;'>
        <h3 style='color: #e2e8f0; font-size: 18px; margin-top: 0;'>Customer Segments & Margins</h3>
        <p style='color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 0;'>
            K-means clustering and RFM analysis identified three customer segments. The <strong style='color: #fff;'>Champions</strong> segment represents the most valuable customers, characterised by high purchase frequency (120.1 orders) and high monetary value ($50,733.60), while Lost customers represent the least active segment. 
            Regression analysis confirmed a statistically significant negative relationship between discount percentages and net revenue. Although 40.6% of transactions occurred with zero discount, higher discount levels were strictly associated with lower profit margins.
        </p>
    </div>

    <div style='background-color: rgba(16, 185, 129, 0.05); padding: 1.5rem; border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 4px;'>
        <h3 style='color: #10b981; font-size: 18px; margin-top: 0;'>Key Recommendations</h3>
        <p style='color: #94a3b8; font-size: 15px; line-height: 1.6; margin-bottom: 0;'>
            Overall, the analysis identified <strong>pricing, discounting, customer retention, and payment collection</strong> as the key areas requiring improvement. 
            The Revenue Analytics Application provides valuable insights to support better business decision making and improve future revenue performance.
        </p>
    </div>
</div>
""")
            
        else:
            st.info(f"The {tabs} tab is currently under construction.")

elif selection == "Customer Analytics":
    render_customer_analytics()
elif selection == "Product & Channel":
    render_product_and_channel()
elif selection == "Pricing & Discount":
    render_pricing_and_discount()
elif selection == "Revenue Forecasting":
    render_revenue_forecasting()
elif selection == "Leakage & Underperformance":
    render_leakage_and_underperformance()
elif selection == "Recommendations":
    render_recommendations()
