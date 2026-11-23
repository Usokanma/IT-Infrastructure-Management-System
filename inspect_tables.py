import sqlite3

database = "database/it_support.db"

connection = sqlite3.connect(database)

tables = connection.execute(
    "SELECT name FROM sqlite_master WHERE type = ?",
    ("table",)
).fetchall()

print("DATABASE TABLES:")

for table in tables:
    print("-", table[0])

connection.close()