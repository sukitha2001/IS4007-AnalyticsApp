import pandas as pd
import streamlit as st
from pathlib import Path

# Use the absolute path or relative to app.py
DATA_DIR = Path(__file__).parent.parent / "generated_data"

@st.cache_data
def load_data():
    """Loads and caches all necessary datasets."""
    try:
        sales = pd.read_csv(DATA_DIR / "sales_transactions.csv")
        sales['transaction_date'] = pd.to_datetime(sales['transaction_date'])
        
        customers = pd.read_csv(DATA_DIR / "customers.csv")
        customers['customer_since'] = pd.to_datetime(customers['customer_since'])
        
        products = pd.read_csv(DATA_DIR / "products.csv")
        campaigns = pd.read_csv(DATA_DIR / "campaigns.csv")
        
        return sales, customers, products, campaigns
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
