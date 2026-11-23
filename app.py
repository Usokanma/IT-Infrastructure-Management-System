import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DATABASE = "database/it_support.db"

# All configurations match your existing SQLite database.
MODULES = {
    "Users": {
        "table": "users",
        "pk": "user_id",
        "fields": [
            ("full_name", "Full Name", "text", True),
            ("department", "Department", "text", True),
            ("email", "Email", "text", False),
            ("role", "Role", "choice", True,
             ["Administrator", "Engineer", "Technician", "User"])
        ]
    },
    "Assets": {
        "table": "assets",
        "pk": "asset_id",
        "fields": [
            ("asset_name", "Asset Name", "text", True),
            ("asset_type", "Asset Type", "text", True),
            ("serial_number", "Serial Number", "text", False),
            ("status", "Status", "choice", True,
             ["Available", "Assigned", "Deployed"]),
            ("assigned_to", "Assigned To", "fk", False,
             "users", "full_name")
        ]
    },
    "Network Devices": {
        "table": "network_devices",
        "pk": "device_id",
        "fields": [
            ("device_name", "Device Name", "text", True),
            ("device_type", "Device Type", "text", True),
            ("ip_address", "IP Address", "text", False),
            ("location", "Location", "text", False),
            ("asset_id", "Related Asset", "fk", False,
             "assets", "asset_name")
        ]
    },
    "Support Tickets": {
        "table": "support_tickets",
        "pk": "ticket_id",
        "fields": [
            ("issue_title", "Issue Title", "text", True),
            ("description", "Description", "text", False),
            ("priority", "Priority", "choice", False,
             ["Low", "Medium", "High", "Critical"]),
            ("status", "Status", "choice", False,
             ["Open", "In Progress", "Resolved", "Closed"]),
            ("reported_by", "Reported By", "fk", True,
             "users", "full_name"),
            ("assigned_to", "Assigned To", "fk", False,
             "users", "full_name"),
            ("asset_id", "Related Asset", "fk", False,
             "assets", "asset_name")
        ],
        "extra": ["created_at"]
    },
    "Maintenance": {
        "table": "maintenance_records",
        "pk": "maintenance_id",
        "fields": [
            ("asset_id", "Asset", "fk", True,
             "assets", "asset_name"),
            ("maintenance_type", "Maintenance Type", "text", True),
            ("description", "Description", "text", False),
            ("maintenance_date", "Maintenance Date", "text", False),
            ("performed_by", "Performed By", "fk", False,
             "users", "full_name")
        ]
    }
}


def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


class ITManagementApp:

    def __init__(self, root):
        self.root = root
        self.root.title("IT Infrastructure Management System")
        self.root.geometry("1150x700")
        self.root.minsize(950, 550)
        self.root.configure(bg="#f1f4f8")

        self.sidebar = tk.Frame(root, bg="#172b4d", width=225)
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

        for name in MODULES:
            self.add_nav_button(
                name,
                lambda module=name: self.show_module(module)
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
                for name, config in MODULES.items():
                    count = conn.execute(
                        f"SELECT COUNT(*) FROM {config['table']}"
                    ).fetchone()[0]

                    card = tk.Frame(
                        self.content,
                        bg="white",
                        padx=25,
                        pady=15,
                        highlightbackground="#d9e0e9",
                        highlightthickness=1
                    )
                    card.pack(fill="x", padx=35, pady=6)

                    tk.Label(
                        card,
                        text=name,
                        font=("Arial", 12),
                        bg="white",
                        fg="#526078"
                    ).pack(anchor="w")

                    tk.Label(
                        card,
                        text=str(count),
                        font=("Arial", 22, "bold"),
                        bg="white",
                        fg="#172b4d"
                    ).pack(anchor="w")

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def show_module(self, module):
        self.clear_content()

        config = MODULES[module]
        table = config["table"]
        pk = config["pk"]

        tk.Label(
            self.content,
            text=module,
            font=("Arial", 24, "bold"),
            bg="#f1f4f8",
            fg="#172b4d"
        ).pack(anchor="w", padx=25, pady=20)

        toolbar = tk.Frame(self.content, bg="#f1f4f8")
        toolbar.pack(fill="x", padx=25, pady=5)

        actions = [
            ("Add New", lambda: self.add_record(module), "#18794e"),
            ("Update Selected", lambda: self.edit_record(module), "#2457a7"),
            ("Delete Selected", lambda: self.delete_record(module), "#b42318"),
            ("Refresh", lambda: self.load_records(module), "#526078")
        ]

        for label, command, color in actions:
            tk.Button(
                toolbar,
                text=label,
                command=command,
                bg=color,
                fg="white",
                padx=12,
                pady=8
            ).pack(side="left", padx=4)

        columns = [pk] + [field[0] for field in config["fields"]]

        if "extra" in config:
            columns += config["extra"]

        self.current_table = ttk.Treeview(
            self.content,
            columns=columns,
            show="headings"
        )

        for column in columns:
            self.current_table.heading(
                column,
                text=column.replace("_", " ").title()
            )
            self.current_table.column(column, width=135, minwidth=90)

        self.current_table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.current_module = module
        self.load_records(module)

    def load_records(self, module):
        config = MODULES[module]
        table = config["table"]

        for item in self.current_table.get_children():
            self.current_table.delete(item)

        columns = [config["pk"]] + [
            field[0] for field in config["fields"]
        ]

        if "extra" in config:
            columns += config["extra"]

        try:
            with connect_db() as conn:
                query = (
                    f"SELECT {', '.join(columns)} "
                    f"FROM {table} ORDER BY {config['pk']}"
                )
                records = conn.execute(query).fetchall()

            for record in records:
                self.current_table.insert("", "end", values=record)

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    def get_selection(self):
        selected = self.current_table.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select a record first."
            )
            return None

        return self.current_table.item(selected[0])["values"]

    def get_fk_options(self, table, display_column):
        with connect_db() as conn:
            rows = conn.execute(
                f"SELECT * FROM {table} ORDER BY 1"
            ).fetchall()

            columns = [
                row[1] for row in conn.execute(
                    f"PRAGMA table_info({table})"
                ).fetchall()
            ]

        id_column = columns[0]
        display_index = columns.index(display_column)

        return [
            (str(row[0]), f"{row[0]} - {row[display_index]}")
            for row in rows
        ]

    def record_dialog(self, module, record=None):
        config = MODULES[module]

        window = tk.Toplevel(self.root)
        window.title("Update Record" if record else "Add Record")
        window.geometry("480x600")
        window.configure(bg="#f1f4f8")
        window.transient(self.root)
        window.grab_set()

        entries = {}
        row = 0

        for index, field in enumerate(config["fields"]):
            column, label, kind, required = field[:4]

            tk.Label(
                window,
                text=label + (" *" if required else ""),
                bg="#f1f4f8",
                font=("Arial", 10, "bold")
            ).grid(row=row, column=0, padx=15, pady=9, sticky="w")

            if kind == "choice":
                widget = ttk.Combobox(
                    window,
                    values=field[4],
                    state="readonly",
                    width=30
                )

                if record:
                    widget.set(record[index + 1])
                elif column == "priority":
                    widget.set("Medium")
                elif column == "status":
                    widget.set("Open")
                elif column == "role":
                    widget.set("User")
                elif column == "status" and module == "Assets":
                    widget.set("Available")
                else:
                    widget.set(field[4][0])

            elif kind == "fk":
                options = self.get_fk_options(field[4], field[5])

                values = [""] + [item[1] for item in options]

                widget = ttk.Combobox(
                    window,
                    values=values,
                    state="readonly",
                    width=30
                )

                if record and record[index + 1] is not None:
                    current_id = str(record[index + 1])
                    for option_id, display in options:
                        if option_id == current_id:
                            widget.set(display)
                            break

                entries[column] = (widget, options, required)

            else:
                widget = tk.Entry(window, width=33)

                if record and record[index + 1] is not None:
                    widget.insert(0, str(record[index + 1]))

            if kind != "fk":
                entries[column] = (widget, None, required)

            widget.grid(row=row, column=1, padx=15, pady=9)
            row += 1

        def save():
            values = []

            for field in config["fields"]:
                column, label, kind, required = field[:4]
                widget, options, _ = entries[column]
                value = widget.get().strip()

                if required and not value:
                    messagebox.showwarning(
                        "Required Field",
                        f"{label} is required.",
                        parent=window
                    )
                    return

                if kind == "fk":
                    if value:
                        matching = [
                            option[0] for option in options
                            if option[1] == value
                        ]
                        if not matching:
                            messagebox.showwarning(
                                "Invalid Selection",
                                f"Select a valid {label}.",
                                parent=window
                            )
                            return
                        value = matching[0]
                    else:
                        value = None

                elif not value:
                    value = None

                values.append(value)

            try:
                with connect_db() as conn:
                    table = config["table"]
                    columns = [
                        field[0] for field in config["fields"]
                    ]

                    if record:
                        assignments = ", ".join(
                            f"{column} = ?" for column in columns
                        )

                        conn.execute(
                            f"UPDATE {table} SET {assignments} "
                            f"WHERE {config['pk']} = ?",
                            values + [record[0]]
                        )

                    else:
                        placeholders = ", ".join(
                            "?" for _ in columns
                        )

                        conn.execute(
                            f"INSERT INTO {table} "
                            f"({', '.join(columns)}) "
                            f"VALUES ({placeholders})",
                            values
                        )

                messagebox.showinfo(
                    "Success",
                    "Record saved successfully.",
                    parent=window
                )

                window.destroy()
                self.load_records(module)

            except sqlite3.Error as error:
                messagebox.showerror(
                    "Database Error",
                    str(error),
                    parent=window
                )

        tk.Button(
            window,
            text="Save Record",
            command=save,
            bg="#18794e",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10
        ).grid(row=row, column=0, columnspan=2, pady=25)

    def add_record(self, module):
        self.record_dialog(module)

    def edit_record(self, module):
        record = self.get_selection()

        if record is not None:
            self.record_dialog(module, record)

    def delete_record(self, module):
        record = self.get_selection()

        if record is None:
            return

        config = MODULES[module]

        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Delete record ID {record[0]}?"
        )

        if not confirm:
            return

        try:
            with connect_db() as conn:
                conn.execute(
                    f"DELETE FROM {config['table']} "
                    f"WHERE {config['pk']} = ?",
                    (record[0],)
                )

            messagebox.showinfo(
                "Success",
                "Record deleted successfully."
            )

            self.load_records(module)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Cannot Delete Record",
                str(error)
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = ITManagementApp(root)
    root.mainloop()