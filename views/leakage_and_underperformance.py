import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header, tabs

def render_leakage_and_underperformance():
    page_header(
        "Revenue Leakage & Underperformance",
        "Spot uncollected revenue, excessive discounting, and low-margin activity that needs management attention.",
        badge="Risk controls",
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
        date_range = st.date_input("Date Range", [min_date, max_date], key="leak_date_filter")
    with f_col2:
        channels = sales['channel'].unique().tolist()
        selected_channels = st.multiselect("Sales Channel", channels, default=channels, key="leak_channel_filter")
    with f_col3:
        categories = products['category'].unique().tolist()
        selected_categories = st.multiselect("Product Category", categories, default=categories, key="leak_category_filter")

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

    # Merge for richer analysis
    df = filtered_sales.merge(products, on='product_id', how='left')
    df_cust = filtered_sales.merge(customers, on='customer_id', how='left')

    # 1. Overdue Revenue
    if 'payment_status' in filtered_sales.columns:
        overdue_sales = df_cust[df_cust['payment_status'] == 'Overdue']
        overdue_amount = overdue_sales['net_revenue'].sum()
    else:
        overdue_amount = 0
        overdue_sales = pd.DataFrame()
        
    # 2. Excessive Discounting (Discount > 15% but low quantity)
    excessive_discount = df[(df['discount_percentage'] > 15) & (df['quantity'] < 5)].copy()
    if not excessive_discount.empty:
        excessive_discount['loss_value'] = excessive_discount['gross_revenue'] - excessive_discount['net_revenue']
        excessive_discount_loss = excessive_discount['loss_value'].sum()
    else:
        excessive_discount_loss = 0
    
    # 3. Low-Margin Sales (Margin < 10%)
    low_margin = df[df['gross_margin'] < (0.10 * df['net_revenue'])]
    low_margin_revenue = low_margin['net_revenue'].sum() if not low_margin.empty else 0
    
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Overdue Revenue", f"${overdue_amount:,.0f}", "Uncollected sales", "$", "negative")
    with col2:
        metric_card("Value Given Away", f"${excessive_discount_loss:,.0f}", "High discount, low volume", "%", "negative")
    with col3:
        metric_card("Low Margin Revenue", f"${low_margin_revenue:,.0f}", "Sales with <10% margin", "!", "negative")
        
    st.write("")
    
    active_tab = tabs("Leakage sections", ["Overdue Details", "Discount Issues", "Low Margin Products"], "leak_tabs", "Overdue Details")
    
    if active_tab == "Overdue Details":
        st.markdown("#### Overdue Revenue Analysis")
        if not overdue_sales.empty:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.write("**Overdue by Customer Type**")
                overdue_by_type = overdue_sales.groupby('customer_type')['net_revenue'].sum().reset_index()
                fig1 = px.bar(overdue_by_type, x='customer_type', y='net_revenue', 
                              color_discrete_sequence=['#ef4444'])
                clean_plotly_layout(fig1, height=350)
                st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
            with c2:
                st.write("**Overdue by Segment**")
                overdue_by_seg = overdue_sales.groupby('segment')['net_revenue'].sum().reset_index()
                fig2 = px.bar(overdue_by_seg, x='segment', y='net_revenue', 
                              color_discrete_sequence=['#f97316'])
                clean_plotly_layout(fig2, height=350)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
                
            st.markdown("#### Overdue Transactions List")
            st.dataframe(overdue_sales[['transaction_id', 'transaction_date', 'customer_id', 'customer_type', 'net_revenue']].head(50), use_container_width=True)
        else:
            st.write("No overdue transactions found.")
            
    elif active_tab == "Discount Issues":
        st.markdown("#### Excessive Discounting (High Discount, Low Volume)")
        if not excessive_discount.empty:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.write("**Value Given Away by Category**")
                loss_by_cat = excessive_discount.groupby('category')['loss_value'].sum().reset_index()
                fig1 = px.bar(loss_by_cat, x='category', y='loss_value', color_discrete_sequence=['#8b5cf6'])
                clean_plotly_layout(fig1, height=350)
                st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
            with c2:
                st.write("**Value Given Away by Channel**")
                loss_by_channel = excessive_discount.groupby('channel')['loss_value'].sum().reset_index()
                fig2 = px.bar(loss_by_channel, x='channel', y='loss_value', color_discrete_sequence=['#db2777'])
                clean_plotly_layout(fig2, height=350)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

            st.markdown("#### Problematic Transactions List")
            st.dataframe(excessive_discount[['transaction_id', 'product_name', 'discount_percentage', 'quantity', 'loss_value']].head(50), use_container_width=True)
        else:
            st.write("No excessive discounting issues found.")
        
    elif active_tab == "Low Margin Products":
        st.markdown("#### Products with Lowest Average Margin")
        margin_by_prod = df.groupby('product_name').agg(
            Avg_Margin_Perc=pd.NamedAgg(column='gross_margin', aggfunc=lambda x: (x.sum() / df.loc[x.index, 'net_revenue'].sum()) * 100 if df.loc[x.index, 'net_revenue'].sum() > 0 else 0),
            Total_Revenue=('net_revenue', 'sum')
        ).reset_index().sort_values('Avg_Margin_Perc').head(10)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.write("**Bottom 10 Products by Margin %**")
            fig = px.bar(margin_by_prod, x='Avg_Margin_Perc', y='product_name', orientation='h', color_discrete_sequence=['#dc2626'])
            fig.update_yaxes(autorange="reversed")
            clean_plotly_layout(fig, height=350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        with c2:
            st.write("**Data Table**")
            st.dataframe(margin_by_prod.style.format({'Avg_Margin_Perc': '{:.2f}%', 'Total_Revenue': '${:,.2f}'}), use_container_width=True, height=350)