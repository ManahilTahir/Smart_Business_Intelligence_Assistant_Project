"""
ProductsPage - Product management page with CRUD operations.
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.components import (create_section_header, create_button, create_table,
                            create_search_bar, COLORS, card_fg)
from utils.validators import Validators
from utils.helpers import Helpers


class ProductsPage:
    """Product management page."""

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

        create_section_header(self.frame, "Product Management",
                               "Add, edit, search, and manage products")

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)

        create_button(top_frame, "➕ Add Product", self._open_add_form,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(top_frame, "✏️ Edit Product", self._open_edit_form,
                      fg_color=COLORS["warning"], hover_color="#E67E22").pack(side="left", padx=5)
        create_button(top_frame, "🗑️ Delete Product", self._delete_product,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(filter_frame, text="Filter by Category:", font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        categories = ["All"] + self.app.product_manager.get_categories()
        self.category_combo = ctk.CTkComboBox(filter_frame, values=categories, height=32, width=180,
                                                command=self._on_filter)
        self.category_combo.set("All")
        self.category_combo.pack(side="left", padx=5)

        create_search_bar(self.frame, self._on_search, "Search by product name, category, ID...")
        self._load_table()

    def _load_table(self, keyword="", category="All"):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if keyword:
            df = self.app.product_manager.search_products(keyword)
        else:
            df = self.app.product_manager.get_all_products()

        if category and category != "All":
            df = df[df["Category"].astype(str) == str(category)] if not df.empty else df

        if df.empty:
            data = []
        else:
            currency = self.app.get_currency()
            data = []
            for _, row in df.iterrows():
                cost = float(row.get("CostPrice", 0))
                selling = float(row.get("SellingPrice", 0))
                data.append({
                    "ProductID": row.get("ProductID", ""),
                    "ProductName": row.get("ProductName", ""),
                    "Category": row.get("Category", ""),
                    "CostPrice": Helpers.format_currency(cost, currency),
                    "SellingPrice": Helpers.format_currency(selling, currency),
                    "Profit/Unit": Helpers.format_currency(selling - cost, currency),
                    "StockQuantity": row.get("StockQuantity", ""),
                    "ReorderLevel": row.get("ReorderLevel", ""),
                })

        self.table_frame = create_table(
            self.frame,
            ["ProductID", "ProductName", "Category", "CostPrice", "SellingPrice", "Profit/Unit", "StockQuantity", "ReorderLevel"],
            data,
        )

    def _on_search(self, keyword):
        self._load_table(keyword.strip(), self.category_combo.get())

    def _on_filter(self, choice):
        self._load_table(self.search_entry.get().strip() if hasattr(self, "search_entry") else "", choice)

    def _open_add_form(self):
        self._show_form_dialog("Add New Product")

    def _open_edit_form(self):
        df = self.app.product_manager.get_all_products()
        if df.empty:
            messagebox.showinfo("Info", "No products to edit.")
            return
        self._show_form_dialog("Edit Product", is_edit=True)

    def _show_form_dialog(self, title, is_edit=False):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title(title)
        dialog.geometry("470x640")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if is_edit:
            id_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            id_frame.pack(fill="x", pady=3)
            ctk.CTkLabel(id_frame, text="Product ID to edit:", font=ctk.CTkFont(size=13)).pack(anchor="w")
            self.prod_id_entry = ctk.CTkEntry(id_frame, placeholder_text="Product ID", height=32)
            self.prod_id_entry.pack(fill="x", pady=2)

            def load_product():
                pid = self.prod_id_entry.get().strip()
                product = self.app.product_manager.get_product_by_id(pid)
                if not product:
                    messagebox.showerror("Error", "Product not found.")
                    return
                self.name_entry.delete(0, "end")
                self.name_entry.insert(0, product.get("ProductName", ""))
                self.cat_combo.set(product.get("Category", ""))
                self.cost_entry.delete(0, "end")
                self.cost_entry.insert(0, str(product.get("CostPrice", "")))
                self.sell_entry.delete(0, "end")
                self.sell_entry.insert(0, str(product.get("SellingPrice", "")))
                self.stock_entry.delete(0, "end")
                self.stock_entry.insert(0, str(product.get("StockQuantity", "")))
                self.reorder_entry.delete(0, "end")
                self.reorder_entry.insert(0, str(product.get("ReorderLevel", "")))

            create_button(id_frame, "Load", load_product, width=70, height=30).pack(side="right", padx=5)

        name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(name_frame, text="Product Name:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(name_frame, placeholder_text="Enter product name", height=32)
        self.name_entry.pack(fill="x", pady=2)

        cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cat_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(cat_frame, text="Category:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        existing_cats = self.app.product_manager.get_categories()
        default_cats = ["Electronics", "Furniture", "Stationery", "Appliances", "Food", "Clothing", "Other"]
        all_cats = sorted(set(existing_cats + default_cats))
        self.cat_combo = ctk.CTkComboBox(cat_frame, values=all_cats, height=32)
        self.cat_combo.set(all_cats[0] if all_cats else "Electronics")
        self.cat_combo.pack(fill="x", pady=2)

        cost_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cost_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(cost_frame, text="Cost Price:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.cost_entry = ctk.CTkEntry(cost_frame, placeholder_text="Enter cost price", height=32)
        self.cost_entry.pack(fill="x", pady=2)

        sell_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        sell_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(sell_frame, text="Selling Price:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.sell_entry = ctk.CTkEntry(sell_frame, placeholder_text="Enter selling price", height=32)
        self.sell_entry.pack(fill="x", pady=2)

        stock_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        stock_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(stock_frame, text="Stock Quantity:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.stock_entry = ctk.CTkEntry(stock_frame, placeholder_text="Enter stock quantity", height=32)
        self.stock_entry.pack(fill="x", pady=2)

        reorder_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        reorder_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(reorder_frame, text="Reorder Level:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.reorder_entry = ctk.CTkEntry(reorder_frame, placeholder_text="Enter reorder level", height=32)
        self.reorder_entry.pack(fill="x", pady=2)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        create_button(btn_frame, "Save", lambda: self._save_product(dialog, is_edit),
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "Cancel", dialog.destroy,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

    def _save_product(self, dialog, is_edit):
        name = self.name_entry.get().strip()
        category = self.cat_combo.get().strip()
        cost = self.cost_entry.get().strip()
        selling = self.sell_entry.get().strip()
        stock = self.stock_entry.get().strip()
        reorder = self.reorder_entry.get().strip()

        errors = Validators.validate_product(name, category, cost, selling, stock, reorder)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            if is_edit:
                pid = self.prod_id_entry.get().strip()
                if not pid:
                    messagebox.showerror("Error", "Please enter a Product ID.")
                    return
                updated = {
                    "ProductName": name, "Category": category,
                    "CostPrice": float(cost), "SellingPrice": float(selling),
                    "StockQuantity": int(stock), "ReorderLevel": int(reorder),
                }
                self.app.product_manager.update_product(pid, updated)
                messagebox.showinfo("Success", "Product updated successfully!")
            else:
                pid = self.app.product_manager.add_product(name, category, cost, selling, stock, reorder)
                messagebox.showinfo("Success", f"Product added! ID: {pid}")

            dialog.destroy()
            self._load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save product: {e}")

    def _delete_product(self):
        df = self.app.product_manager.get_all_products()
        if df.empty:
            messagebox.showinfo("Info", "No products to delete.")
            return

        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Delete Product")
        dialog.geometry("350x150")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter Product ID to delete:", font=ctk.CTkFont(size=14)).pack(pady=20)
        id_entry = ctk.CTkEntry(dialog, placeholder_text="Product ID", height=32, width=200)
        id_entry.pack(pady=5)

        def do_delete():
            pid = id_entry.get().strip()
            if not pid:
                messagebox.showerror("Error", "Please enter a Product ID.")
                return
            if messagebox.askyesno("Confirm", f"Delete product {pid}?"):
                self.app.product_manager.delete_product(pid)
                messagebox.showinfo("Success", "Product deleted successfully!")
                dialog.destroy()
                self._load_table()

        create_button(dialog, "Delete", do_delete,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(pady=10)