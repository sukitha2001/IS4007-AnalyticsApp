import sys
sys.path.append('.')
from utils.data_loader import load_data
sales, customers, products, campaigns = load_data()
recent = sales.sort_values('transaction_date', ascending=False).head(5)
recent = recent.merge(customers, on='customer_id', how='left')
for _, row in recent.iterrows():
    name = f"Customer {str(row['customer_id']).split('-')[-1]}"
    email = f"{name.lower().replace(' ', '.')}@example.com"
    initials = name[:2].upper()
    amount = f"+${row['net_revenue']:,.2f}"
    print(name, email, initials, amount)
print('Done!')
