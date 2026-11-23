import sqlite3

connection = sqlite3.connect("database/it_support.db")

tables = [
    "users",
    "assets",
    "network_devices",
    "support_tickets",
    "maintenance_records"
]

for table in tables:
    print("\nTABLE:", table)
    results = connection.execute(
        f"PRAGMA foreign_key_list({table})"
    ).fetchall()

    if results:
        for relationship in results:
            print(relationship)
    else:
        print("No declared foreign keys")

connection.close()