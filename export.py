import sqlite3
import pandas as pd

def export_clean_data(db_path: str, output_csv_path: str):
    """
    Fetches the sanitized 'clean_sales' table from SQLite
    and exports it to a clean CSV file.
    """
    # 1. Connect to SQLite database
    conn = sqlite3.connect(db_path)
    
    # 2. Load cleaned table into Pandas
    df_clean = pd.read_sql("SELECT * FROM clean_sales", conn)
    conn.close()
    
    # 3. Save as clean CSV (index=False avoids adding extra Pandas row numbers)
    df_clean.to_csv(output_csv_path, index=False)
    
    print(f"✓ Export Complete! Sanitized data exported to '{output_csv_path}'.")

if __name__ == "__main__":
    database = "data/sales_database.db"
    output_file = "data/clean_sales_data.csv"
    
    export_clean_data(database, output_file)