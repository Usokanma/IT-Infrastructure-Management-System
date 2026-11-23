import sqlite3

DATABASE = "database/it_support.db"


def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# 1. CREATE: Register a new asset
def add_asset():
    print("\n--- REGISTER NEW ASSET ---")

    name = input("Asset name: ").strip()
    asset_type = input("Asset type: ").strip()
    serial = input("Serial number: ").strip()
    status = input("Status (Available/Assigned/Deployed): ").strip()

    if not name or not asset_type:
        print("Asset name and type are required.")
        return

    if not status:
        status = "Available"

    try:
        with connect_db() as connection:
            connection.execute("""
                INSERT INTO assets
                (asset_name, asset_type, serial_number, status)
                VALUES (?, ?, ?, ?)
            """, (name, asset_type, serial or None, status))

        print("Asset registered successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


# 2. READ: Display all assets
def view_assets():
    print("\n--- REGISTERED IT ASSETS ---")

    with connect_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT asset_id, asset_name, asset_type,
                   serial_number, status, assigned_to
            FROM assets
        """)

        records = cursor.fetchall()

    if not records:
        print("No assets found.")
        return

    for asset in records:
        print(asset)


# 3. UPDATE: Change asset status
def update_asset():
    print("\n--- UPDATE ASSET STATUS ---")

    try:
        asset_id = int(input("Enter asset ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    new_status = input(
        "Enter new status (Available/Assigned/Deployed): "
    ).strip()

    if new_status not in ("Available", "Assigned", "Deployed"):
        print("Invalid status.")
        return

    with connect_db() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE assets
            SET status = ?
            WHERE asset_id = ?
        """, (new_status, asset_id))

        if cursor.rowcount == 0:
            print("Asset not found.")
        else:
            print("Asset status updated successfully!")


# 4. DELETE: Remove an asset
def delete_asset():
    print("\n--- DELETE ASSET ---")

    try:
        asset_id = int(input("Enter asset ID: "))
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    try:
        with connect_db() as connection:
            cursor = connection.cursor()

            # Check whether another record uses this asset
            for table in (
                "network_devices",
                "support_tickets",
                "maintenance_records"
            ):
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE asset_id = ?",
                    (asset_id,)
                )

                if cursor.fetchone()[0] > 0:
                    print(
                        f"Cannot delete: asset is referenced in {table}."
                    )
                    return

            cursor.execute("""
                DELETE FROM assets
                WHERE asset_id = ?
            """, (asset_id,))

            if cursor.rowcount == 0:
                print("Asset not found.")
            else:
                print("Asset deleted successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


# APPLICATION MENU
def main():
    while True:
        print("\n================================")
        print(" IT ASSET MANAGEMENT SYSTEM")
        print("================================")
        print("1. Register new asset")
        print("2. View all assets")
        print("3. Update asset status")
        print("4. Delete asset")
        print("5. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_asset()
        elif choice == "2":
            view_assets()
        elif choice == "3":
            update_asset()
        elif choice == "4":
            delete_asset()
        elif choice == "5":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()