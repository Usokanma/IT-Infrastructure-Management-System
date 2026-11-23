import sqlite3

connection = sqlite3.connect("database/it_support.db")
cursor = connection.cursor()

# Inspect assets table structure
print("\nASSETS TABLE STRUCTURE")
print("-" * 40)

cursor.execute("""
    SELECT sql
    FROM sqlite_master
    WHERE type = 'table' AND name = 'assets'
""")

print(cursor.fetchone()[0])

# Display current assets
print("\nCURRENT ASSETS")
print("-" * 40)

cursor.execute("SELECT * FROM assets")

for record in cursor.fetchall():
    print(record)

# Display network devices
print("\nNETWORK DEVICES")
print("-" * 40)

cursor.execute("SELECT * FROM network_devices")

for record in cursor.fetchall():
    print(record)

connection.close()