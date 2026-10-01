import os
import generate_data
import extract
import clean
import export

def run_pipeline():
    """
    Master Data Pipeline Execution Flow:
    1. Generate Raw Messy Data
    2. Extract & Ingest to SQLite Staging
    3. Clean & Validate via SQL & Pandas
    4. Export Final Clean File
    """
    print("\n=========================================")
    print("🚀 STARTING ETL DATA CLEANING PIPELINE")
    print("=========================================\n")
    
    # Define system file paths
    raw_csv = "data/raw_sales_data.csv"
    database = "data/sales_database.db"
    sql_script = "clean.sql"
    clean_csv = "data/clean_sales_data.csv"
    
    # Step 1: Generate synthetic messy dataset
    print("[1/4] Generating raw operational data...")
    generate_data.raw_data  # Accessing generator module
    # Run creation logic if raw CSV doesn't exist yet
    df_raw = generate_data.pd.DataFrame(generate_data.raw_data)
    os.makedirs("data", exist_ok=True)
    df_raw.to_csv(raw_csv, index=False)
    print(f"✓ Created raw data file at '{raw_csv}'.\n")
    
    # Step 2: Extract & stage in SQLite
    print("[2/4] Ingesting raw CSV into SQLite staging...")
    extract.load_staging_data(raw_csv, database)
    print()
    
    # Step 3: Run SQL cleaning & validation
    print("[3/4] Running SQL transformations & validation...")
    clean.execute_sql_cleaning(database, sql_script)
    clean.validate_cleaned_data(database)
    print()
    
    # Step 4: Export final clean deliverable
    print("[4/4] Exporting final clean CSV deliverable...")
    export.export_clean_data(database, clean_csv)
    
    print("\n=========================================")
    print("🎉 PIPELINE EXECUTED SUCCESSFULLY!")
    print("=========================================\n")

if __name__ == "__main__":
    run_pipeline()