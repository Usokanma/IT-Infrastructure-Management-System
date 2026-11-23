import sqlite3

# Connect to the database
connection = sqlite3.connect("database/it_support.db")

# Retrieve all database tables
cursor = connection.cursor()

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
""")

tables = cursor.fetchall()

print("DATABASE TABLES:")
for table in tables:
    print("-", table[0])

connection.close()
