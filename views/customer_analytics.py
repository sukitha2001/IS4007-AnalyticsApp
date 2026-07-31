import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data
from utils.theme import apply_theme, clean_plotly_layout, metric_card, page_header, tabs

def render_customer_analytics():
    
    
    page_header(
        "Customer Analytics",
        "Segment customers by recency, frequency, and monetary value to prioritize retention and growth actions.",
        badge="RFM model",
    )
    
    sales, customers, products, campaigns = load_data()
    
    if sales.empty:
        st.warning("Data could not be loaded.")
    else:
        # --- RFM Analysis ---
        latest_date = sales['transaction_date'].max() + pd.Timedelta(days=1)
        
        rfm = sales.groupby('customer_id').agg({
            'transaction_date': lambda x: (latest_date - x.max()).days,
            'transaction_id': 'count',
            'net_revenue': 'sum'
        }).reset_index()
        
        rfm.rename(columns={
            'transaction_date': 'Recency',
            'transaction_id': 'Frequency',
            'net_revenue': 'Monetary'
        }, inplace=True)
        
        # Simple segmentation based on percentiles
        quantiles = rfm.quantile(q=[0.33, 0.66], numeric_only=True)
        
        def r_score(x):
            if x <= quantiles['Recency'][0.33]: return 3
            elif x <= quantiles['Recency'][0.66]: return 2
            else: return 1
            
        def fm_score(x, c):
            if x <= quantiles[c][0.33]: return 1
            elif x <= quantiles[c][0.66]: return 2
            else: return 3
            
        rfm['R'] = rfm['Recency'].apply(r_score)
        rfm['F'] = rfm['Frequency'].apply(fm_score, args=('Frequency',))
        rfm['M'] = rfm['Monetary'].apply(fm_score, args=('Monetary',))
        
        rfm['RFM_Score'] = rfm['R'].map(str) + rfm['F'].map(str) + rfm['M'].map(str)
        
        def segment_customer(df):
            if df['RFM_Score'] == '333':
                return 'Core - Best Customers'
            elif df['F'] == 3:
                return 'Loyal'
            elif df['M'] == 3:
                return 'Big Spenders'
            elif df['R'] == 3:
                return 'New / Active'
            elif df['R'] == 1:
                return 'At Risk / Lost'
            else:
                return 'Regular'
                
        rfm['Segment'] = rfm.apply(segment_customer, axis=1)
        
        # --- UI Layout ---
        total_value = rfm["Monetary"].sum()
        best_segment = rfm.groupby("Segment")["Monetary"].sum().idxmax()
        cols = st.columns(3)
        with cols[0]:
            metric_card("Customer Value", f"${total_value:,.0f}", "Total segment revenue", "$", "positive")
        with cols[1]:
            metric_card("Best Segment", best_segment, "Highest revenue contribution", "◎")
        with cols[2]:
            metric_card("At Risk", f"{(rfm['Segment'] == 'At Risk / Lost').sum():,}", "Customers needing attention", "!", "negative")
    
        st.write("")
        active_tab = tabs("Customer sections", ['RFM Analysis', 'K-Means Clustering', 'Top Customers'], "cust_tabs", 'RFM Analysis')
        

        if active_tab == 'RFM Analysis':
            st.markdown("#### Customer Segmentation")
            seg_counts = rfm['Segment'].value_counts().reset_index()
            seg_counts.columns = ['Segment', 'Count']
            
            col1, col2 = st.columns([1, 1])
            with col1:
                with st.container(border=True):
                    fig_seg = px.pie(seg_counts, values='Count', names='Segment', title="Customer Segments Distribution", hole=0.45)
                    clean_plotly_layout(fig_seg, height=390, showlegend=True)
                    st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})
                
            with col2:
                with st.container(border=True):
                    seg_val = rfm.groupby('Segment')['Monetary'].sum().reset_index().sort_values("Monetary")
                    fig_val = px.bar(seg_val, x='Monetary', y='Segment', orientation='h', title="Revenue by Segment", color_discrete_sequence=["#2563eb"])
                    clean_plotly_layout(fig_val, height=390)
                    st.plotly_chart(fig_val, use_container_width=True, config={"displayModeBar": False})
                
            st.markdown("#### RFM Breakdown")
            fig_scatter = px.scatter(rfm, x='Recency', y='Monetary', size='Frequency', color='Segment', 
                                     hover_data=['customer_id'], title="Recency vs Monetary Value")
            clean_plotly_layout(fig_scatter, height=440, showlegend=True)
            st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})
            st.dataframe(rfm.head(50), use_container_width=True)
            
        elif active_tab == 'K-Means Clustering':
            st.markdown("#### K-Means Clustering")
            st.write("Using Machine Learning to group customers into 3 distinct clusters based on their purchasing behavior, matching the analysis notebook.")
            
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            customer_metrics = sales.groupby('customer_id').agg(
                total_spend=('net_revenue', 'sum'),
                order_count=('transaction_id', 'nunique'),
                avg_order_value=('net_revenue', 'mean'),
                total_items=('quantity', 'sum')
            ).reset_index()
            
            customer_metrics.fillna(0, inplace=True)
            X = customer_metrics[['total_spend', 'order_count', 'avg_order_value']]
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            optimal_k = 3
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            customer_metrics['cluster'] = kmeans.fit_predict(X_scaled)
            customer_metrics['cluster'] = customer_metrics['cluster'].astype(str)
            
            # Map clusters to names based on total spend
            cluster_avg = customer_metrics.groupby('cluster')['total_spend'].mean().sort_values()
            cluster_map = {
                cluster_avg.index[0]: 'Cluster 1: Low Spend',
                cluster_avg.index[1]: 'Cluster 2: Mid Spend',
                cluster_avg.index[2]: 'Cluster 3: High Spend'
            }
            customer_metrics['Cluster_Name'] = customer_metrics['cluster'].map(cluster_map)
            
            fig_km = px.scatter(customer_metrics, x='order_count', y='total_spend', color='Cluster_Name',
                                   title="Customer Segments: Spend vs. Order Count", opacity=0.8,
                                   color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981'])
            clean_plotly_layout(fig_km, height=450, showlegend=True)
            st.plotly_chart(fig_km, use_container_width=True, config={"displayModeBar": False})
            
            st.markdown("**Cluster Summary**")
            cluster_summary = customer_metrics.groupby('Cluster_Name').agg({
                'total_spend': 'mean',
                'order_count': 'mean',
                'avg_order_value': 'mean',
                'customer_id': 'count'
            }).reset_index()
            
            cluster_summary.columns = ['Cluster', 'Avg Total Spend', 'Avg Order Count', 'Avg Order Value', 'Customer Count']
            st.dataframe(cluster_summary, use_container_width=True)
        elif active_tab == 'Top Customers':
            st.markdown("#### Top Customers by Revenue")
            top_cust = rfm.sort_values('Monetary', ascending=False).head(10)
            top_cust_details = top_cust.merge(customers, on='customer_id', how='left')
            st.dataframe(top_cust_details[['customer_id', 'customer_type', 'location_category', 'Monetary', 'Frequency']], use_container_width=True)
    