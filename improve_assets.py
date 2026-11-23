import sqlite3

connection = sqlite3.connect("database/it_support.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

try:
    # 1. Mark the Cisco Router as deployed infrastructure
    cursor.execute("""
        UPDATE assets
        SET status = 'Deployed', assigned_to = NULL
        WHERE serial_number = 'CISCO001'
    """)

    # 2. Register the Office Switch as an organisational asset
    cursor.execute("""
        INSERT OR IGNORE INTO assets
        (asset_name, asset_type, serial_number, status, assigned_to)
        VALUES (?, ?, ?, ?, ?)
    """, ("Office Switch", "Switch", "SWITCH001", "Deployed", None))

    # 3. Retrieve the switch asset ID
    cursor.execute("""
        SELECT asset_id FROM assets
        WHERE serial_number = 'SWITCH001'
    """)

    switch_result = cursor.fetchone()

    if switch_result is None:
        raise ValueError("Office Switch asset could not be found.")

    switch_asset_id = switch_result[0]

    # 4. Link the network device to its asset
    cursor.execute("""
        UPDATE network_devices
        SET asset_id = ?
        WHERE device_name = 'Office Switch'
    """, (switch_asset_id,))

    if cursor.rowcount == 0:
        raise ValueError("Office Switch network device was not found.")

    connection.commit()

    print("Asset improvements completed successfully!")

except Exception as error:
    connection.rollback()
    print("An error occurred:", error)

finally:
    connection.close()