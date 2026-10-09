"""
CustomersPage - Customer management page with CRUD operations.
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.components import (create_section_header, create_button, create_table,
                            create_search_bar, COLORS, card_fg)
from utils.validators import Validators
from utils.helpers import Helpers


class CustomersPage:
    """Customer management page."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self._build_layout()

    def hide(self):
        self.frame.pack_forget()

    def _build_layout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        create_section_header(self.frame, "Customer Management",
                               "Add, edit, search, and manage customer records")

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)

        create_button(top_frame, "➕ Add Customer", self._open_add_form,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(top_frame, "✏️ Edit Customer", self._open_edit_form,
                      fg_color=COLORS["warning"], hover_color="#E67E22").pack(side="left", padx=5)
        create_button(top_frame, "🗑️ Delete Customer", self._delete_customer,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

        create_search_bar(self.frame, self._on_search, "Search by name, phone, email, city...")
        self._load_table()

    def _load_table(self, keyword=""):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if keyword:
            df = self.app.customer_manager.search_customers(keyword)
        else:
            df = self.app.customer_manager.get_all_customers()

        if df.empty:
            data = []
        else:
            currency = self.app.get_currency()
            data = []
            for _, row in df.iterrows():
                data.append({
                    "CustomerID": row.get("CustomerID", ""),
                    "CustomerName": row.get("CustomerName", ""),
                    "Phone": row.get("Phone", ""),
                    "Email": row.get("Email", ""),
                    "City": row.get("City", ""),
                    "TotalPurchases": Helpers.format_currency(row.get("TotalPurchases", 0), currency),
                })

        self.table_frame = create_table(
            self.frame,
            ["CustomerID", "CustomerName", "Phone", "Email", "City", "TotalPurchases"],
            data,
        )

    def _on_search(self, keyword):
        self._load_table(keyword.strip())

    def _open_add_form(self):
        self._show_form_dialog("Add New Customer")

    def _open_edit_form(self):
        df = self.app.customer_manager.get_all_customers()
        if df.empty:
            messagebox.showinfo("Info", "No customers to edit.")
            return
        self._show_form_dialog("Edit Customer", is_edit=True)

    def _show_form_dialog(self, title, is_edit=False):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title(title)
        dialog.geometry("450x500")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if is_edit:
            id_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            id_frame.pack(fill="x", pady=3)
            ctk.CTkLabel(id_frame, text="Customer ID to edit:", font=ctk.CTkFont(size=13)).pack(anchor="w")
            self.cust_id_entry = ctk.CTkEntry(id_frame, placeholder_text="Customer ID", height=32)
            self.cust_id_entry.pack(fill="x", pady=2)

            def load_customer():
                cid = self.cust_id_entry.get().strip()
                customer = self.app.customer_manager.get_customer_by_id(cid)
                if not customer:
                    messagebox.showerror("Error", "Customer not found.")
                    return
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, customer.get("CustomerName", ""))
                self.phone_entry.delete(0, "end")
                self.phone_entry.insert(0, str(customer.get("Phone", "")))
                self.email_entry.delete(0, "end")
                self.email_entry.insert(0, str(customer.get("Email", "")))
                self.city_entry.delete(0, "end")
                self.city_entry.insert(0, str(customer.get("City", "")))

            create_button(id_frame, "Load", load_customer, width=70, height=30).pack(side="right", padx=5)

        name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(name_frame, text="Customer Name:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter customer name", height=32)
        self.name_entry.pack(fill="x", pady=2)

        phone_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        phone_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(phone_frame, text="Phone:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.phone_entry = ctk.CTkEntry(phone_frame, placeholder_text="Enter phone number", height=32)
        self.phone_entry.pack(fill="x", pady=2)

        email_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        email_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(email_frame, text="Email:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(email_frame, placeholder_text="Enter email address", height=32)
        self.email_entry.pack(fill="x", pady=2)

        city_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        city_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(city_frame, text="City:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.city_entry = ctk.CTkEntry(city_frame, placeholder_text="Enter city", height=32)
        self.city_entry.pack(fill="x", pady=2)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        create_button(btn_frame, "Save", lambda: self._save_customer(dialog, is_edit),
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "Cancel", dialog.destroy,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

    def _save_customer(self, dialog, is_edit):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        city = self.city_entry.get().strip()

        errors = Validators.validate_customer(name, phone, email)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            if is_edit:
                cid = self.cust_id_entry.get().strip()
                if not cid:
                    messagebox.showerror("Error", "Please enter a Customer ID.")
                    return
                updated = {
                    "CustomerName": name, "Phone": phone,
                    "Email": email, "City": city,
                }
                self.app.customer_manager.update_customer(cid, updated)
                messagebox.showinfo("Success", "Customer updated successfully!")
            else:
                cid = self.app.customer_manager.add_customer(name, phone, email, city)
                messagebox.showinfo("Success", f"Customer added! ID: {cid}")

            dialog.destroy()
            self._load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save customer: {e}")

    def _delete_customer(self):
        df = self.app.customer_manager.get_all_customers()
        if df.empty:
            messagebox.showinfo("Info", "No customers to delete.")
            return

        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Delete Customer")
        dialog.geometry("350x150")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter Customer ID to delete:", font=ctk.CTkFont(size=14)).pack(pady=20)
        id_entry = ctk.CTkEntry(dialog, placeholder_text="Customer ID", height=32, width=200)
        id_entry.pack(pady=5)

        def do_delete():
            cid = id_entry.get().strip()
            if not cid:
                messagebox.showerror("Error", "Please enter a Customer ID.")
                return
            if messagebox.askyesno("Confirm", f"Delete customer {cid}?"):
                self.app.customer_manager.delete_customer(cid)
                messagebox.showinfo("Success", "Customer deleted successfully!")
                dialog.destroy()
                self._load_table()

        create_button(dialog, "Delete", do_delete,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(pady=10)