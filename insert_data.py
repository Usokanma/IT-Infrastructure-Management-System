import sqlite3

connection = sqlite3.connect("database/it_support.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

# 1. Register staff members
staff = [
    ("David Okafor", "IT Support", "david@gmail.com", "Technician"),
    ("Sarah Johnson", "Broadcast Technology", "sarah@gmail.com", "Engineer"),
    ("Emmanuel Andrew", "Network Operations", "Emmanuel@gmail.com", "Administrator"),
    ("Chuka-Oditah Usokanma", "IT Support", "usokanmachukaoditah@gmail.com", "Administrator")
]

for person in staff:
    cursor.execute("""
        INSERT OR IGNORE INTO users
        (full_name, department, email, role)
        VALUES (?, ?, ?, ?)
    """, person)

# Retrieve staff IDs
cursor.execute("SELECT user_id, full_name FROM users")
users = {name: user_id for user_id, name in cursor.fetchall()}

# 2. Register IT equipment
assets = [
    ("HP EliteBook", "Laptop", "HP001", "Assigned", users["Chuka-Oditah Usokanma"]),
    ("Dell OptiPlex", "Desktop", "DELL001", "Available", None),
    ("Cisco Router", "Router", "CISCO001", "Assigned", None)
]

for asset in assets:
    cursor.execute("""
        INSERT OR IGNORE INTO assets
        (asset_name, asset_type, serial_number, status, assigned_to)
        VALUES (?, ?, ?, ?, ?)
    """, asset)

# Retrieve equipment IDs
cursor.execute("SELECT asset_id, serial_number FROM assets")
equipment = {serial: asset_id for asset_id, serial in cursor.fetchall()}

# 3. Register network devices
devices = [
    ("Main Office Router", "Router", "192.168.1.1",
     "Main Office", equipment["CISCO001"]),
    ("Office Switch", "Switch", "192.168.1.2",
     "Network Room", None)
]

for device in devices:
    cursor.execute("""
        INSERT OR IGNORE INTO network_devices
        (device_name, device_type, ip_address, location, asset_id)
        VALUES (?, ?, ?, ?, ?)
    """, device)

# 4. Register technical support tickets
tickets = [
    ("Network connectivity issue",
     "Unable to connect to the office network.",
     "High", "Open",
     users["Chuka-Oditah Usokanma"],
     users["Emmanuel Andrew"],
     equipment["HP001"]),

    ("Computer maintenance request",
     "Desktop requires routine servicing.",
     "Medium", "In Progress",
     users["Sarah Johnson"],
     users["Chuka-Oditah Usokanma"],
     equipment["DELL001"])
]

for ticket in tickets:
    cursor.execute("""
        SELECT ticket_id FROM support_tickets
        WHERE issue_title = ? AND reported_by = ?
    """, (ticket[0], ticket[4]))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO support_tickets
            (issue_title, description, priority, status,
             reported_by, assigned_to, asset_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ticket)

# 5. Register maintenance records
maintenance = [
    (equipment["HP001"], "Software maintenance",
     "Operating system and software updates.",
     users["Chuka-Oditah Usokanma"]),

    (equipment["CISCO001"], "Network maintenance",
     "Router configuration inspection.",
     users["Emmanuel Andrew"])
]

for record in maintenance:
    cursor.execute("""
        SELECT maintenance_id FROM maintenance_records
        WHERE asset_id = ? AND maintenance_type = ?
    """, (record[0], record[1]))

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO maintenance_records
            (asset_id, maintenance_type, description, performed_by)
            VALUES (?, ?, ?, ?)
        """, record)

connection.commit()
connection.close()

print("Sample organisational records inserted successfully!")
