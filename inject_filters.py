import re

with open('app.py', 'r') as f:
    content = f.read()

# Define the new filter section
filter_section = """        if tabs == 'Overview':
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

            if filtered_sales.empty:
                st.warning("No data available for the selected filters.")
            else:
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
"""

# Find where 'if tabs == 'Overview':' starts
start_idx = content.find("        if tabs == 'Overview':")
end_idx = content.find("            cols = st.columns(4)")

# We need to replace the start block
if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + filter_section + content[end_idx:]
    
    # Now we need to replace all occurrences of `sales` with `filtered_sales`
    # inside the 'else:' block for the Overview tab.
    # The 'else:' block ends at '        else:\n            st.info(f"The {tabs} tab is currently under construction.")'
    
    overview_end_idx = new_content.find("        else:\n            st.info(f\"The {tabs} tab is currently under construction.\")")
    
    if overview_end_idx != -1:
        # We need to add one indent level to everything inside the new 'else:' block (from cols = st.columns(4) to end of overview block)
        # But wait, python requires proper indentation.
        
        # Let's extract the code to be indented and modified
        block_to_modify = new_content[end_idx:overview_end_idx]
        
        # Indent everything by 4 spaces
        indented_block = "\n".join(["    " + line if line.strip() else line for line in block_to_modify.split("\n")])
        
        # Replace 'sales[' with 'filtered_sales[' and 'sales.' with 'filtered_sales.'
        indented_block = re.sub(r'\bsales\[', 'filtered_sales[', indented_block)
        indented_block = re.sub(r'\bsales\.', 'filtered_sales.', indented_block)
        indented_block = re.sub(r'\bsales = ', 'filtered_sales = ', indented_block) # In case there's an assignment, though there shouldn't be
        
        # Reconstruct the final string
        final_content = new_content[:end_idx] + indented_block + new_content[overview_end_idx:]
        
        with open('app.py', 'w') as f:
            f.write(final_content)
