import sqlite3

# Connect to the database
connection = sqlite3.connect("database/it_support.db")
cursor = connection.cursor()

# Retrieve all application tables
cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
AND name NOT LIKE 'sqlite_%'
""")

tables = cursor.fetchall()

# Display each table's structure
for table in tables:
    table_name = table[0]

    print("\nTABLE:", table_name)

    cursor.execute(f"PRAGMA table_info({table_name})")

    columns = cursor.fetchall()

    for column in columns:
        print(column)

connection.close()