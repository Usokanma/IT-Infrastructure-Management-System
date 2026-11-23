import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

DATABASE = "database/it_support.db"


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


class ITManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title("IT Infrastructure Management System")
        self.root.geometry("1100x650")
        self.root.minsize(900, 550)

        self.root.configure(bg="#f1f4f8")

        self.sidebar = tk.Frame(root, bg="#172b4d", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = tk.Frame(root, bg="#f1f4f8")
        self.content.pack(side="right", fill="both", expand=True)

        tk.Label(
            self.sidebar,
            text="IT INFRASTRUCTURE\nMANAGEMENT",
            bg="#172b4d",
            fg="white",
            font=("Arial", 15, "bold"),
            pady=30
        ).pack()

        self.add_nav_button("Dashboard", self.show_dashboard)
        self.add_nav_button("Asset Management", self.show_assets)

        self.add_nav_button(
            "Network Devices",
            lambda: self.coming_soon("Network Devices")
        )
        
        self.add_nav_button("User Management", self.show_users)
        self.add_nav_button(
            "Support Tickets",
            lambda: self.coming_soon("Support Tickets")
        )
        self.add_nav_button(
            "Maintenance",
            lambda: self.coming_soon("Maintenance")
        )

        self.show_dashboard()

    def add_nav_button(self, text, command):
        tk.Button(
            self.sidebar,
            text=text,
            command=command,
            bg="#243b60",
            fg="white",
            activebackground="#345582",
            activeforeground="white",
            font=("Arial", 11),
            relief="flat",
            anchor="w",
            padx=20,
            pady=14
        ).pack(fill="x", padx=10, pady=4)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def coming_soon(self, module):
        self.clear_content()
        tk.Label(
            self.content,
            text=module,
            font=("Arial", 24, "bold"),
            bg="#f1f4f8"
        ).pack(pady=40)

        tk.Label(
            self.content,
            text="This module will be connected next.",
            font=("Arial", 13),
            bg="#f1f4f8"
        ).pack()

    def show_dashboard(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Dashboard",
            font=("Arial", 25, "bold"),
            bg="#f1f4f8",
            fg="#172b4d"
        ).pack(anchor="w", padx=30, pady=25)

        try:
            with connect_db() as conn:
                cursor = conn.cursor()

                tables = [
                    ("Total Assets", "assets"),
                    ("Network Devices", "network_devices"),
                    ("Registered Users", "users"),
                    ("Support Tickets", "support_tickets"),
                    ("Maintenance Records", "maintenance_records")
                ]

                for index, (label, table) in enumerate(tables):
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]

                    card = tk.Frame(
                        self.content,
                        bg="white",
                        padx=25,
                        pady=25,
                        highlightbackground="#d9e0e9",
                        highlightthickness=1
                    )

                    card.pack(
                        fill="x",
                        padx=35,
                        pady=8
                    )

                    tk.Label(
                        card,
                        text=label,
                        font=("Arial", 12),
                        bg="white",
                        fg="#526078"
                    ).pack(anchor="w")

                    tk.Label(
                        card,
                        text=str(count),
                        font=("Arial", 23, "bold"),
                        bg="white",
                        fg="#172b4d"
                    ).pack(anchor="w")

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def show_assets(self):
        self.clear_content()

        tk.Label(
            self.content,
            text="Asset Management",
            font=("Arial", 24, "bold"),
            bg="#f1f4f8",
            fg="#172b4d"
        ).pack(anchor="w", padx=25, pady=20)

        toolbar = tk.Frame(self.content, bg="#f1f4f8")
        toolbar.pack(fill="x", padx=25, pady=5)

        tk.Button(
            toolbar, text="Add Asset",
            command=self.add_asset,
            bg="#18794e", fg="white",
            padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="Update Status",
            command=self.update_asset,
            bg="#2457a7", fg="white",
            padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="Delete Asset",
            command=self.delete_asset,
            bg="#b42318", fg="white",
            padx=15, pady=8
        ).pack(side="left", padx=5)

        tk.Button(
            toolbar, text="Refresh",
            command=self.load_assets,
            padx=15, pady=8
        ).pack(side="left", padx=5)

        columns = (
            "ID", "Name", "Type",
            "Serial", "Status", "Assigned To"
        )

        self.asset_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.asset_table.heading(column, text=column)
            self.asset_table.column(column, width=125)

        self.asset_table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.load_assets()

    def load_assets(self):
        for item in self.asset_table.get_children():
            self.asset_table.delete(item)

        try:
            with connect_db() as conn:
                records = conn.execute("""
                    SELECT asset_id, asset_name, asset_type,
                           serial_number, status, assigned_to
                    FROM assets
                    ORDER BY asset_id
                """).fetchall()

            for record in records:
                self.asset_table.insert("", "end", values=record)

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def selected_asset(self):
        selected = self.asset_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an asset first."
            )
            return None

        return self.asset_table.item(selected[0])["values"]

    def add_asset(self):
        name = simpledialog.askstring("New Asset", "Asset name:")
        if name is None:
            return

        asset_type = simpledialog.askstring("New Asset", "Asset type:")
        if asset_type is None:
            return

        if not name.strip() or not asset_type.strip():
            messagebox.showwarning(
                "Required Fields",
                "Asset name and type are required."
            )
            return

        serial = simpledialog.askstring(
            "New Asset", "Serial number (optional):"
        )

        if serial is None:
            return

        status = simpledialog.askstring(
            "New Asset",
            "Status (Available/Assigned/Deployed):",
            initialvalue="Available"
        )

        if status is None:
            return

        if status not in ("Available", "Assigned", "Deployed"):
            messagebox.showwarning("Invalid Status", "Invalid asset status.")
            return

        try:
            with connect_db() as conn:
                conn.execute("""
                    INSERT INTO assets
                    (asset_name, asset_type, serial_number, status)
                    VALUES (?, ?, ?, ?)
                """, (
                    name.strip(),
                    asset_type.strip(),
                    serial.strip() or None,
                    status
                ))

            messagebox.showinfo("Success", "Asset registered successfully.")
            self.load_assets()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def update_asset(self):
        asset = self.selected_asset()

        if asset is None:
            return

        new_status = simpledialog.askstring(
            "Update Asset",
            "Enter new status (Available/Assigned/Deployed):",
            initialvalue=asset[4]
        )

        if new_status is None:
            return

        if new_status not in ("Available", "Assigned", "Deployed"):
            messagebox.showwarning("Invalid Status", "Invalid status.")
            return

        try:
            with connect_db() as conn:
                cursor = conn.execute("""
                    UPDATE assets
                    SET status = ?
                    WHERE asset_id = ?
                """, (new_status, asset[0]))

            if cursor.rowcount:
                messagebox.showinfo("Success", "Asset updated successfully.")
            else:
                messagebox.showwarning("Not Found", "Asset not found.")

            self.load_assets()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def delete_asset(self):
        asset = self.selected_asset()

        if asset is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete {asset[1]} (ID: {asset[0]})?"
        )

        if not confirm:
            return

        try:
            with connect_db() as conn:
                cursor = conn.cursor()

                for table in (
                    "network_devices",
                    "support_tickets",
                    "maintenance_records"
                ):
                    cursor.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE asset_id = ?",
                        (asset[0],)
                    )

                    if cursor.fetchone()[0] > 0:
                        messagebox.showwarning(
                            "Cannot Delete",
                            f"This asset is referenced in {table}."
                        )
                        return

                cursor.execute(
                    "DELETE FROM assets WHERE asset_id = ?",
                    (asset[0],)
                )

            messagebox.showinfo("Success", "Asset deleted successfully.")
            self.load_assets()

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))


if __name__ == "__main__":
    root = tk.Tk()
    app = ITManagementApp(root)
    root.mainloop()