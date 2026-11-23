import sqlite3

connection = sqlite3.connect("database/it_support.db")
cursor = connection.cursor()

tables = [
    "users",
    "assets",
    "network_devices",
    "support_tickets",
    "maintenance_records"
]

for table in tables:
    print("\n" + "=" * 50)
    print(f"TABLE: {table.upper()}")
    print("=" * 50)

    cursor.execute(f"SELECT * FROM {table}")

    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))

    records = cursor.fetchall()

    if records:
        for record in records:
            print(record)
    else:
        print("No records found.")

connection.close()
