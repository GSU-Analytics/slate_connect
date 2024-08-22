# example.py

import pandas as pd
from slate_connect import SlateSQLConnection
from config import username, database, hostname, port, driver

def main():
    # Instantiate the class
    connection = SlateSQLConnection(username, database, hostname, port, driver)

    query = """
    -- Orientation status counts since April 1, 2024
    SELECT
        COALESCE(r.[status], 'register') AS status,
        COUNT(*) AS status_count
    FROM [form.response] r 
    INNER JOIN [form] f ON (f.[id] = r.[form]) 
    LEFT OUTER JOIN [form] fp ON (fp.[id] = f.[parent])
    WHERE f.[type] = 'event' 
    AND ISNULL(f.[scope], fp.[scope]) = 'application'
    AND f.date > '2024-04-01'
    AND COALESCE(r.[status], 'register') IN ('register', 'attend', 'noshow', 'cancel')
    AND LOWER(f.category) LIKE '%orientation%'
    AND r.[record] IS NOT NULL
    GROUP BY COALESCE(r.[status], 'register')
    ORDER BY status
    """

    df = connection.execute_query(query)
    df.to_csv('example.csv', index=False)
        
if __name__ == "__main__":
    main()