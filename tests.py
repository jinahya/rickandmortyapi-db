# Python Script to Find Whitespace-Only Values


import sqlite3

# Connect to your SQLite database file
# Replace 'your_database.db' with your actual database file name
conn = sqlite3.connect("rickandmortyapi.db")
cursor = conn.cursor()

# Query the sqlite_master table to get all user-defined table names
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
)
tables = cursor.fetchall()

for table_name_tuple in tables:
    table_name = table_name_tuple[0]
    print(f"\n--- Checking table: {table_name} ---")

    # Query the pragma_table_info to get column names for the current table
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    columns_info = cursor.fetchall()

    # Filter for columns that are likely to be text and store their names
    # The 'type' might be 'TEXT', 'VARCHAR', etc.
    text_columns = [
        col[1]
        for col in columns_info
        if "TEXT" in col[2].upper() or "CHAR" in col[2].upper()
    ]

    for column_name in text_columns:
        # Construct the dynamic SQL query to find rows where the trimmed column is an empty string
        # TRIM(column_name) = '' identifies values that are only whitespace after trimming
        query = f"SELECT rowid, * FROM '{table_name}' WHERE TRIM('{column_name}') = '' AND '{column_name}' IS NOT NULL;"

        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            print(f"  Found whitespace-only values in column '{column_name}':")
            for row in rows:
                print(
                    f"    Row ID {row[0]}: {row[columns_info.index((0, column_name, '', 0, None, 0)) + 1]!r}"
                )  # Display the raw value

conn.close()
