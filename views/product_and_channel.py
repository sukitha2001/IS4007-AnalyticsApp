import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header

def render_product_and_channel():
    
    
    page_header(
        "Product & Channel Revenue Analysis",
        "Compare product performance, category contribution, and channel profitability in a compact operating view.",
        badge="Portfolio view",
    )
    
    sales, customers, products, campaigns = load_data()
    
    if sales.empty:
        st.warning("Data could not be loaded.")
    else:
        # --- FILTERS ---
        st.markdown("<h3 style='color: gray; font-size: 14px; text-transform: uppercase; margin-bottom: 0px;'>Page Filters</h3>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3 = st.columns(3)
        
        min_date = sales['transaction_date'].min().date()
        max_date = sales['transaction_date'].max().date()
        with f_col1:
            date_range = st.date_input("Date Range", [min_date, max_date], key="pc_date_filter")
        with f_col2:
            channels = sales['channel'].unique().tolist()
            selected_channels = st.multiselect("Sales Channel", channels, default=channels, key="pc_channel_filter")
        with f_col3:
            categories = products['category'].unique().tolist()
            selected_categories = st.multiselect("Product Category", categories, default=categories, key="pc_category_filter")

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
    
        top_channel = df.groupby("channel")["net_revenue"].sum().idxmax()
        top_product = df.groupby("product_name")["net_revenue"].sum().idxmax()
        channel_count = df["channel"].nunique()
        cols = st.columns(3)
        with cols[0]:
            metric_card("Top Channel", top_channel, "Highest net revenue", "▣", "positive")
        with cols[1]:
            metric_card("Top Product", top_product, "Best revenue performer", "▦", "positive")
        with cols[2]:
            metric_card("Channels", f"{channel_count:,}", "Active sales routes", "◎")
    
        st.write("")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.markdown("#### Top Performing Products")
                prod_rev = df.groupby('product_name')['net_revenue'].sum().reset_index().sort_values('net_revenue', ascending=False)
                fig_top = px.bar(prod_rev.head(10), x='net_revenue', y='product_name', orientation='h', title="Top 10 Products by Revenue", color_discrete_sequence=["#2563eb"])
                fig_top.update_yaxes(autorange="reversed")
                clean_plotly_layout(fig_top, height=430)
                st.plotly_chart(fig_top, use_container_width=True, config={"displayModeBar": False})
            
        with col2:
            with st.container(border=True):
                st.markdown("#### Low Performing Products")
                fig_low = px.bar(prod_rev.tail(10), x='net_revenue', y='product_name', orientation='h', title="Bottom 10 Products by Revenue", color_discrete_sequence=['#dc2626'])
                fig_low.update_yaxes(autorange="reversed")
                clean_plotly_layout(fig_low, height=430)
                st.plotly_chart(fig_low, use_container_width=True, config={"displayModeBar": False})
            
        st.write("")
        
        st.markdown("#### Channel Profitability & Revenue")
        
        channel_metrics = df.groupby('channel').agg(
            Revenue=('net_revenue', 'sum'),
            Margin=('gross_margin', 'sum'),
            Transactions=('transaction_id', 'count')
        ).reset_index()
        
        channel_metrics['Margin %'] = (channel_metrics['Margin'] / channel_metrics['Revenue']) * 100
        
        col3, col4 = st.columns(2)
        with col3:
            with st.container(border=True):
                fig_ch_rev = px.bar(channel_metrics, x='channel', y=['Revenue', 'Margin'], barmode='group', title="Revenue vs Margin by Channel", color_discrete_sequence=["#2563eb", "#16a34a"])
                clean_plotly_layout(fig_ch_rev, height=370, showlegend=True)
                st.plotly_chart(fig_ch_rev, use_container_width=True, config={"displayModeBar": False})
            
        with col4:
            st.dataframe(channel_metrics.style.format({'Revenue': '${:,.2f}', 'Margin': '${:,.2f}', 'Margin %': '{:.2f}%'}), use_container_width=True)
    