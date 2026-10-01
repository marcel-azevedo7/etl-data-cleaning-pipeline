import sqlite3
import pandas as pd

def execute_sql_cleaning(db_path: str, sql_file: str):
    """Reads and executes the SQL script against our SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_file, 'r') as file:
        sql_script = file.read()
        
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✓ SQL cleaning script executed successfully.")

def validate_cleaned_data(db_path: str):
    """Loads the clean_sales table into Pandas to verify data quality."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM clean_sales", conn)
    conn.close()

    print("\n--- Data Validation Summary ---")
    print(f"Total Clean Records: {len(df)}")
    print(f"Duplicate IDs:       {df['transaction_id'].duplicated().sum()}")
    print(f"Null Emails:         {df['customer_email'].isnull().sum()}")
    print(f"Refund Count:        {(df['transaction_type'] == 'REFUND').sum()}")
    print("\nSample Cleaned Data:")
    print(df)

if __name__ == "__main__":
    database = "data/sales_database.db"
    sql_script_path = "clean.sql"
    
    execute_sql_cleaning(database, sql_script_path)
    validate_cleaned_data(database)