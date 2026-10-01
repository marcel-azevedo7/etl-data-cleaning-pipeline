-- Clean & Transform Staging Sales Data into Production Table
DROP TABLE IF EXISTS clean_sales;

CREATE TABLE clean_sales AS
WITH cleaned_fields AS (
    SELECT 
        -- 1. If transaction_id is missing, generate a fallback key
        COALESCE(transaction_id, 'UNKNOWN_' || ROW_NUMBER() OVER (ORDER BY sale_date)) AS transaction_id,
        
        TRIM(customer_name) AS customer_name,
        TRIM(LOWER(customer_email)) AS customer_email,
        
        -- 2. Strip '$', ',', and accounting parentheses '()' for negative numbers
        CAST(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE(sale_amount, '$', ''), 
                    ',', ''), 
                '(', '-'), 
            ')', '') 
        AS REAL) AS sale_amount,
        
        -- 3. Categorize transaction type so refunds are accounted for properly
        CASE 
            WHEN sale_amount LIKE '%(%' OR sale_amount LIKE '-%' THEN 'REFUND'
            ELSE 'SALE'
        END AS transaction_type,
        
        -- 4. Standardize MM/DD/YYYY to YYYY-MM-DD using PRINTF for padding
        CASE 
            WHEN sale_date LIKE '%/%/%' THEN 
                SUBSTR(sale_date, 7, 4) || '-' || 
                PRINTF('%02d', CAST(SUBSTR(sale_date, 1, 2) AS INTEGER)) || '-' || 
                PRINTF('%02d', CAST(SUBSTR(sale_date, 4, 2) AS INTEGER))
            ELSE sale_date
        END AS sale_date,
        
        -- 5. Deduplicate based on transaction_id or customer_name
        ROW_NUMBER() OVER (
            PARTITION BY COALESCE(transaction_id, customer_name) 
            ORDER BY sale_date DESC
        ) AS row_num
    FROM stg_sales_raw
)
SELECT 
    transaction_id,
    customer_name,
    customer_email,
    sale_amount,
    transaction_type,
    sale_date
FROM cleaned_fields
WHERE row_num = 1; -- Keeps deduplicated sales AND retains refunds & missing IDs!