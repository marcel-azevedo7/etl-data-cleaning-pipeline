import sqlite3
import pandas as pd

def load_staging_data(csv_path: str, db_path: str):
    """
    Reads the raw CSV data and loads it into a SQLite database staging table.
    We import all columns as text (strings) so no raw data is altered or lost.
    """
    # 1. Connect to SQLite database (it will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    # 2. Read the raw CSV file using Pandas (dtype=str keeps raw strings intact)
    df_raw = pd.read_csv(csv_path, dtype=str)
    
    # 3. Write the DataFrame into a SQLite staging table named 'stg_sales_raw'
    df_raw.to_sql("stg_sales_raw", conn, if_exists="replace", index=False)
    
    # 4. Close the connection
    conn.close()
    
    print(f"✓ Success! Raw CSV loaded into SQLite staging table 'stg_sales_raw' in '{db_path}'.")

if __name__ == "__main__":
    # Define file paths
    raw_csv = "data/raw_sales_data.csv"
    database = "data/sales_database.db"
    
    # Run extraction function
    load_staging_data(raw_csv, database)