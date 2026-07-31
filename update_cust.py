import re

with open("views/customer_analytics.py", "r") as f:
    content = f.read()

# Replace tabs definition
content = content.replace(
    "active_tab = tabs(\"Customer sections\", ['Segments & Value', 'RFM Analysis', 'Top Customers'], \"cust_tabs\", 'Segments & Value')",
    "active_tab = tabs(\"Customer sections\", ['RFM Analysis', 'K-Means Clustering', 'Top Customers'], \"cust_tabs\", 'RFM Analysis')"
)

# Extract and Replace blocks
# The block starts at `if active_tab == 'Segments & Value':` and ends before `elif active_tab == 'Top Customers':`
# I will use a regex to replace this entire section.

new_tabs_code = """
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
            st.markdown("#### K-Means Clustering on RFM")
            st.write("Using Machine Learning to group customers into 3 distinct clusters based on their purchasing behavior.")
            
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            
            rfm_ml = rfm[['Recency', 'Frequency', 'Monetary']].copy()
            scaler = StandardScaler()
            rfm_scaled = scaler.fit_transform(rfm_ml)
            
            kmeans = KMeans(n_clusters=3, random_state=42)
            rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)
            rfm['Cluster'] = rfm['Cluster'].astype(str)
            
            # Map clusters to names based on monetary value
            cluster_avg = rfm.groupby('Cluster')['Monetary'].mean().sort_values()
            cluster_map = {
                cluster_avg.index[0]: 'Cluster 1: Low Value',
                cluster_avg.index[1]: 'Cluster 2: Mid Value',
                cluster_avg.index[2]: 'Cluster 3: High Value'
            }
            rfm['Cluster_Name'] = rfm['Cluster'].map(cluster_map)
            
            fig_km = px.scatter_3d(rfm, x='Recency', y='Frequency', z='Monetary', color='Cluster_Name',
                                   title="3D K-Means Clustering", opacity=0.7,
                                   color_discrete_sequence=['#ef4444', '#f59e0b', '#10b981'])
            fig_km.update_layout(margin=dict(l=0, r=0, b=0, t=30), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_km, use_container_width=True)
            
            st.markdown("**Cluster Summary**")
            cluster_summary = rfm.groupby('Cluster_Name').agg({
                'Recency': 'mean',
                'Frequency': 'mean',
                'Monetary': ['mean', 'count']
            }).reset_index()
            cluster_summary.columns = ['Cluster', 'Avg Recency', 'Avg Frequency', 'Avg Monetary', 'Customer Count']
            st.dataframe(cluster_summary, use_container_width=True)
"""

pattern = r"        if active_tab == 'Segments & Value':.*?(?=        elif active_tab == 'Top Customers':)"
content = re.sub(pattern, new_tabs_code, content, flags=re.DOTALL)

with open("views/customer_analytics.py", "w") as f:
    f.write(content)
