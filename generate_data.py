import os
import pandas as pd

# 1. Create the 'data' folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# 2. Define sample raw data with deliberate operational errors
raw_data = {
    "transaction_id": ["TXN101", "TXN102", "TXN103", "TXN103", "TXN104", "TXN105", None],
    "customer_name": ["  Alice Smith ", "BOB JONES", "Charlie Brown", "Charlie Brown", "David Miller", "  Eva Green ", "Frank Wright"],
    "customer_email": ["alice@EXAMPLE.com", "bob@gmail.com", "charlie@outlook.com", "charlie@outlook.com", "DAVID@DOM.COM", "eva@domain.com", "frank@domain.com"],
    "sale_amount": ["$150.00", "$200.50", "$50.00", "$50.00", "-$10.00", "$1,200.00", "$300.00"],
    "sale_date": ["2026-09-01", "09/02/2026", "2026-09-03", "2026-09-03", "2026-09-04", "09/05/2026", "2026-09-06"]
}

# 3. Save as CSV
df = pd.DataFrame(raw_data)
csv_path = "data/raw_sales_data.csv"
df.to_csv(csv_path, index=False)

print(f"✓ Synthetic raw dataset created successfully at '{csv_path}'!")