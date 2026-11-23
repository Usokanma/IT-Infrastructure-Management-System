import sqlite3

conn = sqlite3.connect("database/it_support.db")

conn.execute(
    "DELETE FROM assets WHERE asset_id = ?",
    (10,)
)

conn.commit()

print("Asset deleted successfully.")

conn.close()
