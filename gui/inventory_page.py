"""
InventoryPage - Inventory management page showing stock status.
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.components import (create_section_header, create_button, create_table,
                            create_search_bar, COLORS, card_fg)
from utils.helpers import Helpers


class InventoryPage:
    """Inventory management page."""

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

        create_section_header(self.frame, "Inventory Management",
                               "View stock levels and restock products")

        inv = self.app.inventory_manager
        stats_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=5)

        in_stock = inv.get_in_stock_count()
        low_stock = inv.get_low_stock_count()
        out_stock = inv.get_out_of_stock_count()
        total_value = inv.get_total_inventory_value()
        currency = self.app.get_currency()

        for label, count, color in [
            ("In Stock", in_stock, COLORS["success"]),
            ("Low Stock", low_stock, COLORS["warning"]),
            ("Out of Stock", out_stock, COLORS["danger"]),
        ]:
            badge = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                 border_width=1, border_color=COLORS["border"])
            badge.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(badge, text=label, font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=(8, 0))
            ctk.CTkLabel(badge, text=str(count), font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=color).pack(pady=(2, 8))

        value_badge = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                    border_width=1, border_color=COLORS["border"])
        value_badge.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        ctk.CTkLabel(value_badge, text="Inventory Value", font=ctk.CTkFont(size=13),
                     text_color=COLORS["text_light"]).pack(pady=(8, 0))
        ctk.CTkLabel(value_badge, text=Helpers.format_currency(total_value, currency),
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(2, 8))

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)
        create_button(top_frame, "📦 Restock Product", self._restock_dialog,
                      fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"]).pack(side="left", padx=5)

        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(filter_frame, text="Select Product:", font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        prod_names = ["All"] + self.app.product_manager.get_product_names()
        self._prod_filter_combo = ctk.CTkComboBox(filter_frame, values=prod_names, height=32, width=200,
                                                  command=self._on_prod_filter)
        self._prod_filter_combo.set("All")
        self._prod_filter_combo.pack(side="left", padx=5)

        create_search_bar(self.frame, self._on_search, "Search by product name, category, ID...")
        self._load_table()

    def _on_prod_filter(self, choice):
        self._load_table("")

    def _load_table(self, keyword=""):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        prod_filter = self._prod_filter_combo.get() if hasattr(self, "_prod_filter_combo") else "All"

        if keyword:
            df = self.app.inventory_manager.search_inventory(keyword)
        else:
            df = self.app.inventory_manager.get_inventory()

        if not df.empty and prod_filter != "All":
            df = df[df["ProductName"].astype(str) == str(prod_filter)]

        if df.empty:
            data = []
        else:
            data = []
            for _, row in df.iterrows():
                data.append({
                    "ProductID": row.get("ProductID", ""),
                    "ProductName": row.get("ProductName", ""),
                    "Category": row.get("Category", ""),
                    "StockQuantity": row.get("StockQuantity", ""),
                    "ReorderLevel": row.get("ReorderLevel", ""),
                    "StockStatus": row.get("StockStatus", ""),
                })

        self.table_frame = create_table(
            self.frame,
            ["ProductID", "ProductName", "Category", "StockQuantity", "ReorderLevel", "StockStatus"],
            data,
        )

    def _on_search(self, keyword):
        self._load_table(keyword.strip())

    def _restock_dialog(self):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Restock Product")
        dialog.geometry("420x280")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Restock Product", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(20, 10))

        product_names = self.app.product_manager.get_product_names()
        if not product_names:
            ctk.CTkLabel(dialog, text="No products available.").pack(pady=20)
            return

        ctk.CTkLabel(dialog, text="Product:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=50)
        prod_combo = ctk.CTkComboBox(dialog, values=product_names, height=32, width=300)
        prod_combo.set(product_names[0])
        prod_combo.pack(pady=5)

        ctk.CTkLabel(dialog, text="Quantity to add:", font=ctk.CTkFont(size=13)).pack(anchor="w", padx=50)
        qty_entry = ctk.CTkEntry(dialog, placeholder_text="Enter quantity", height=32, width=300)
        qty_entry.pack(pady=5)

        def do_restock():
            product_name = prod_combo.get()
            qty = qty_entry.get().strip()
            try:
                qty_int = int(qty)
                if qty_int <= 0:
                    messagebox.showerror("Error", "Quantity must be positive.")
                    return
                pid = self.app.product_manager.get_product_id_by_name(product_name)
                self.app.inventory_manager.restock_product(pid, qty_int)
                messagebox.showinfo("Success", f"Restocked {product_name} with {qty_int} units.")
                dialog.destroy()
                self._build_layout()
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a valid integer.")

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        create_button(btn_frame, "💾 Save", do_restock,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "Cancel", dialog.destroy,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)