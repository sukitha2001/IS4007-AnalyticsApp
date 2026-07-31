import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header

def render_pricing_and_discount():
    page_header(
        "Pricing and Discount Analysis",
        "Assess whether discounts are supporting revenue growth or quietly eroding gross margin.",
        badge="Commercial controls",
    )
    
    sales, customers, products, campaigns = load_data()
    
    if sales.empty:
        st.warning("Data could not be loaded.")
        return

    # --- FILTERS ---
    st.markdown("<h3 style='color: gray; font-size: 14px; text-transform: uppercase; margin-bottom: 0px;'>Page Filters</h3>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    
    min_date = sales['transaction_date'].min().date()
    max_date = sales['transaction_date'].max().date()
    with f_col1:
        date_range = st.date_input("Date Range", [min_date, max_date], key="pd_date_filter")
    with f_col2:
        channels = sales['channel'].unique().tolist()
        selected_channels = st.multiselect("Sales Channel", channels, default=channels, key="pd_channel_filter")
    with f_col3:
        categories = products['category'].unique().tolist()
        selected_categories = st.multiselect("Product Category", categories, default=categories, key="pd_category_filter")

    filtered_sales = sales.copy()
    
    if len(date_range) == 2:
        filtered_sales = filtered_sales[(filtered_sales['transaction_date'].dt.date >= date_range[0]) & (filtered_sales['transaction_date'].dt.date <= date_range[1])]
        
    if selected_channels:
        filtered_sales = filtered_sales[filtered_sales['channel'].isin(selected_channels)]
        
    if selected_categories:
        filtered_products = products[products['category'].isin(selected_categories)]
        filtered_sales = filtered_sales[filtered_sales['product_id'].isin(filtered_products['product_id'])]
        
    st.write("") # Spacing after filters
    
    if filtered_sales.empty:
        st.warning("No data available for the selected filters.")
        return

    # Create discount bands
    bins = [-1, 0, 5, 10, 15, 20, 100]
    labels = ['0%', '1-5%', '6-10%', '11-15%', '16-20%', '>20%']
    filtered_sales['discount_band'] = pd.cut(filtered_sales['discount_percentage'], bins=bins, labels=labels)

    avg_discount = filtered_sales["discount_percentage"].mean()
    discount_cost = filtered_sales["gross_revenue"].sum() - filtered_sales["net_revenue"].sum()
    high_discount_sales = (filtered_sales["discount_percentage"] > 15).sum()

    cols = st.columns(3)
    with cols[0]:
        metric_card("Average Discount", f"{avg_discount:.1f}", "Weighted across transactions", "%")
    with cols[1]:
        metric_card("Discount Value", f"{discount_cost:,.0f}", "Gross revenue given away", "$", "negative")
    with cols[2]:
        metric_card("High Discount Sales", f"{high_discount_sales:,}", "Transactions above 15%", "negative")

    st.write("")
    
    df = filtered_sales.merge(products, on='product_id', how='left')
    df_cust = filtered_sales.merge(customers, on='customer_id', how='left')

    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("#### Discount Impact on Customer Lifetime Value")
            # Aggregation by customer
            cust_clv = df_cust.groupby('customer_id').agg(
                Total_Spend=('net_revenue', 'sum'),
                Avg_Discount=('discount_percentage', 'mean')
            ).reset_index()
            # Sample to prevent browser lag if too many customers
            if len(cust_clv) > 2000:
                cust_clv = cust_clv.sample(2000, random_state=42)
                
            fig_clv = px.scatter(cust_clv, x='Avg_Discount', y='Total_Spend', opacity=0.6,
                                 title="Higher discounts don't always mean higher CLV",
                                 color_discrete_sequence=["#8b5cf6"], trendline="ols")
            fig_clv.update_traces(marker=dict(size=8, line=dict(width=1, color='white')))
            clean_plotly_layout(fig_clv, height=380)
            st.plotly_chart(fig_clv, use_container_width=True, config={"displayModeBar": False})
        
    with col2:
        with st.container(border=True):
            st.markdown("#### Revenue vs. Discount Cost by Segment")
            df_cust['discount_value'] = df_cust['gross_revenue'] - df_cust['net_revenue']
            seg_agg = df_cust.groupby('segment').agg(
                Net_Revenue=('net_revenue', 'sum'),
                Discount_Value=('discount_value', 'sum')
            ).reset_index()
            
            seg_melt = seg_agg.melt(id_vars='segment', value_vars=['Net_Revenue', 'Discount_Value'],
                                    var_name='Metric', value_name='Amount')
            
            fig_bar = px.bar(seg_melt, x='segment', y='Amount', color='Metric', barmode='group',
                             title="Are discounts proportional to revenue brought in?",
                             color_discrete_map={'Net_Revenue': '#3b82f6', 'Discount_Value': '#ef4444'})
            
            fig_bar.update_layout(legend_title_text='')
            newnames = {'Net_Revenue': 'Net Revenue', 'Discount_Value': 'Discount Cost'}
            fig_bar.for_each_trace(lambda t: t.update(name = newnames.get(t.name, t.name)))

            clean_plotly_layout(fig_bar, height=380, showlegend=True)
            # Move legend to top to save space
            fig_bar.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
            
    st.write("")
    col3, col4 = st.columns(2)

    with col3:
        with st.container(border=True):
            st.markdown("#### Margin Erosion by Product Category")
            margin_impact = df.groupby('category').agg(
                Avg_Discount=('discount_percentage', 'mean'),
                Avg_Margin=('gross_margin', 'mean'),
                Total_Revenue=('net_revenue', 'sum')
            ).reset_index()
            
            fig_bubble = px.scatter(margin_impact, x='Avg_Discount', y='Avg_Margin', size='Total_Revenue', color='category',
                                    title="Categories with high discounts & low margins", size_max=45,
                                    color_discrete_sequence=px.colors.qualitative.Prism)
            fig_bubble.add_hline(y=margin_impact['Avg_Margin'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Margin")
            fig_bubble.add_vline(x=margin_impact['Avg_Discount'].mean(), line_dash="dash", line_color="gray", annotation_text="Avg Discount")
            clean_plotly_layout(fig_bubble, height=440, showlegend=True)
            st.plotly_chart(fig_bubble, use_container_width=True, config={"displayModeBar": False})

    with col4:
        with st.container(border=True):
            st.markdown("#### Revenue by Discount Band")
            rev_by_band = filtered_sales.groupby('discount_band', observed=False)['net_revenue'].sum().reset_index()
            fig_band = px.bar(rev_by_band, x='discount_band', y='net_revenue', 
                              title="How much revenue falls into each discount bucket?", 
                              color='discount_band', color_discrete_sequence=px.colors.sequential.Blues[2:])
            clean_plotly_layout(fig_band, height=440, showlegend=False)
            st.plotly_chart(fig_band, use_container_width=True, config={"displayModeBar": False})