"""
SalesPage - Sales management page with CRUD operations.
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.components import (create_section_header, create_button, create_table,
                            create_search_bar, COLORS, card_fg)
from utils.validators import Validators
from utils.helpers import Helpers


class SalesPage:
    """Sales management page."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.selected_sale_id = None

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self._build_layout()

    def hide(self):
        self.frame.pack_forget()

    def _build_layout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        create_section_header(self.frame, "Sales Management",
                               "Add, view, search, and manage sales records")

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)

        create_button(top_frame, "➕ Add Sale", self._open_add_form,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(top_frame, "✏️ Update Sale", self._open_update_form,
                      fg_color=COLORS["warning"], hover_color="#E67E22").pack(side="left", padx=5)
        create_button(top_frame, "🗑️ Delete Sale", self._delete_sale,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

        search_frame, self.search_entry = create_search_bar(self.frame, self._on_search,
                                                             "Search by product, customer, date...")
        self._load_table()

    def _load_table(self, keyword=""):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if keyword:
            df = self.app.sales_manager.search_sales(keyword)
        else:
            df = self.app.sales_manager.get_all_sales()

        if df.empty:
            data = []
        else:
            currency = self.app.get_currency()
            data = []
            for _, row in df.iterrows():
                data.append({
                    "SaleID": row.get("SaleID", ""),
                    "Date": row.get("Date", ""),
                    "Product": row.get("Product", ""),
                    "Customer": row.get("Customer", ""),
                    "Quantity": row.get("Quantity", ""),
                    "UnitPrice": Helpers.format_currency(row.get("UnitPrice", 0), currency),
                    "TotalAmount": Helpers.format_currency(row.get("TotalAmount", 0), currency),
                    "PaymentMethod": row.get("PaymentMethod", ""),
                })

        self.table_frame = create_table(
            self.frame,
            ["SaleID", "Date", "Product", "Customer", "Quantity", "UnitPrice", "TotalAmount", "PaymentMethod"],
            data,
        )

    def _on_search(self, keyword):
        self._load_table(keyword.strip())

    def _open_add_form(self):
        self._show_form_dialog("Add New Sale")

    def _open_update_form(self):
        df = self.app.sales_manager.get_all_sales()
        if df.empty:
            messagebox.showinfo("Info", "No sales records to update.")
            return
        self._show_form_dialog("Update Sale", is_update=True)

    def _show_form_dialog(self, title, is_update=False):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title(title)
        dialog.geometry("450x520")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        product_names = self.app.product_manager.get_product_names()
        customer_names = self.app.customer_manager.get_customer_names()
        payment_methods = self.app.sales_manager.get_payment_methods()

        sale_id_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        sale_id_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(sale_id_frame, text="Sale ID (for update):", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.sale_id_entry = ctk.CTkEntry(sale_id_frame, placeholder_text="Enter Sale ID to update", height=32)
        self.sale_id_entry.pack(fill="x", pady=2)

        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(date_frame, text="Date (YYYY-MM-DD):", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD", height=32)
        self.date_entry.insert(0, Helpers.today_string())
        self.date_entry.pack(fill="x", pady=2)

        prod_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        prod_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(prod_frame, text="Product:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.product_combo = ctk.CTkComboBox(prod_frame, values=product_names, height=32)
        if product_names:
            self.product_combo.set(product_names[0])
        self.product_combo.pack(fill="x", pady=2)

        cust_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cust_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(cust_frame, text="Customer:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.customer_combo = ctk.CTkComboBox(cust_frame, values=customer_names, height=32)
        if customer_names:
            self.customer_combo.set(customer_names[0])
        self.customer_combo.pack(fill="x", pady=2)

        qty_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        qty_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(qty_frame, text="Quantity:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.qty_entry = ctk.CTkEntry(qty_frame, placeholder_text="Enter quantity", height=32)
        self.qty_entry.pack(fill="x", pady=2)

        price_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        price_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(price_frame, text="Unit Price:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.price_entry = ctk.CTkEntry(price_frame, placeholder_text="Enter unit price", height=32)
        self.price_entry.pack(fill="x", pady=2)

        pay_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        pay_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(pay_frame, text="Payment Method:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.payment_combo = ctk.CTkComboBox(pay_frame, values=payment_methods, height=32)
        self.payment_combo.set(payment_methods[0] if payment_methods else "")
        self.payment_combo.pack(fill="x", pady=2)

        def on_product_change(choice):
            price = self.app.product_manager.get_selling_price_by_name(choice)
            self.price_entry.delete(0, "end")
            self.price_entry.insert(0, str(price))
        self.product_combo.bind("<<ComboboxSelected>>", lambda e: on_product_change(self.product_combo.get()))
        on_product_change(self.product_combo.get())

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        create_button(btn_frame, "Save", lambda: self._save_sale(dialog, is_update),
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "Cancel", dialog.destroy,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

    def _save_sale(self, dialog, is_update):
        date = self.date_entry.get().strip()
        product = self.product_combo.get().strip()
        customer = self.customer_combo.get().strip()
        quantity = self.qty_entry.get().strip()
        unit_price = self.price_entry.get().strip()
        payment = self.payment_combo.get().strip()

        errors = Validators.validate_sale(date, product, customer, quantity, unit_price, payment)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            if is_update:
                sale_id = self.sale_id_entry.get().strip()
                if not sale_id:
                    messagebox.showerror("Error", "Please enter a Sale ID to update.")
                    return
                updated = {
                    "Date": date, "Product": product, "Customer": customer,
                    "Quantity": int(quantity), "UnitPrice": float(unit_price),
                    "PaymentMethod": payment,
                }
                self.app.sales_manager.update_sale(sale_id, updated)
                messagebox.showinfo("Success", f"Sale {sale_id} updated successfully!")
            else:
                sale_id = self.app.sales_manager.add_sale(
                    date, product, customer, quantity, unit_price, payment
                )
                self.app.product_manager.reduce_stock(product, int(quantity))
                cust_id = self.app.customer_manager.get_customer_id_by_name(customer)
                total = float(quantity) * float(unit_price)
                self.app.customer_manager.update_total_purchases(cust_id, total)
                messagebox.showinfo("Success", f"Sale added successfully! ID: {sale_id}")

            dialog.destroy()
            self._load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save sale: {e}")

    def _delete_sale(self):
        df = self.app.sales_manager.get_all_sales()
        if df.empty:
            messagebox.showinfo("Info", "No sales records to delete.")
            return

        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Delete Sale")
        dialog.geometry("350x150")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter Sale ID to delete:", font=ctk.CTkFont(size=14)).pack(pady=20)
        id_entry = ctk.CTkEntry(dialog, placeholder_text="Sale ID", height=32, width=200)
        id_entry.pack(pady=5)

        def do_delete():
            sale_id = id_entry.get().strip()
            if not sale_id:
                messagebox.showerror("Error", "Please enter a Sale ID.")
                return
            if messagebox.askyesno("Confirm", f"Delete sale {sale_id}?"):
                self.app.sales_manager.delete_sale(sale_id)
                messagebox.showinfo("Success", "Sale deleted successfully!")
                dialog.destroy()
                self._load_table()

        create_button(dialog, "Delete", do_delete,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(pady=10)