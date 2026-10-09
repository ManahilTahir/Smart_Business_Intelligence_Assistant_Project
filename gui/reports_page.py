"""
ReportsPage - Reports page showing sales, expense, profit, and inventory reports.
"""

import customtkinter as ctk
from gui.components import (create_section_header, create_table, COLORS, card_fg)
from utils.helpers import Helpers


class ReportsPage:
    """Reports page with business reports."""

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

        create_section_header(self.frame, "Reports",
                               "Generated business reports from current data")

        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)

        tabview.add("Sales Report")
        tabview.add("Expense Report")
        tabview.add("Profit Report")
        tabview.add("Inventory Report")

        self._build_sales_report(tabview.tab("Sales Report"))
        self._build_expense_report(tabview.tab("Expense Report"))
        self._build_profit_report(tabview.tab("Profit Report"))
        self._build_inventory_report(tabview.tab("Inventory Report"))

    def _build_sales_report(self, tab):
        analyzer = self.app.analyzer
        currency = self.app.get_currency()
        sales = analyzer.get_sales_analysis()

        info_frame = ctk.CTkFrame(tab, fg_color=card_fg(), corner_radius=10,
                                  border_width=1, border_color=COLORS["border"])
        info_frame.pack(fill="x", padx=10, pady=10)

        best = analyzer.get_best_selling_product()
        best_name = best["ProductName"] if best else "N/A"
        best_qty = int(best["QuantitySold"]) if best else 0

        for label, value in [
            ("Total Sales", Helpers.format_currency(sales["total_sales"], currency)),
            ("Average Sale", Helpers.format_currency(sales["average_sale"], currency)),
            ("Total Quantity Sold", str(sales["total_quantity"])),
            ("Best Selling Product", f"{best_name} ({best_qty} units)"),
        ]:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(side="left", pady=5)
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white").pack(side="right", pady=5)

        ctk.CTkLabel(tab, text="Sales by Category:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        cat_data = []
        if not sales["sales_by_category"].empty:
            for _, row in sales["sales_by_category"].iterrows():
                cat_data.append({"Category": row["Category"], "TotalSales": Helpers.format_currency(row["TotalSales"], currency)})
        create_table(tab, ["Category", "TotalSales"], cat_data)

    def _build_expense_report(self, tab):
        analyzer = self.app.analyzer
        currency = self.app.get_currency()
        exp = analyzer.get_expense_analysis()

        info_frame = ctk.CTkFrame(tab, fg_color=card_fg(), corner_radius=10,
                                  border_width=1, border_color=COLORS["border"])
        info_frame.pack(fill="x", padx=10, pady=10)

        highest = analyzer.get_highest_expense_category()
        highest_cat = highest["Category"] if highest else "N/A"
        highest_amt = Helpers.format_currency(highest["TotalAmount"], currency) if highest else "N/A"

        for label, value in [
            ("Total Expenses", Helpers.format_currency(exp["total_expenses"], currency)),
            ("Average Expense", Helpers.format_currency(exp["average_expense"], currency)),
            ("Highest Expense Category", f"{highest_cat} ({highest_amt})"),
        ]:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(side="left", pady=5)
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white").pack(side="right", pady=5)

        ctk.CTkLabel(tab, text="Expenses by Category:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        cat_data = []
        if not exp["expenses_by_category"].empty:
            for _, row in exp["expenses_by_category"].iterrows():
                cat_data.append({"Category": row["Category"], "TotalAmount": Helpers.format_currency(row["TotalAmount"], currency)})
        create_table(tab, ["Category", "TotalAmount"], cat_data)

    def _build_profit_report(self, tab):
        analyzer = self.app.analyzer
        currency = self.app.get_currency()

        revenue = analyzer.calculate_revenue()
        cogs = analyzer.calculate_cost_of_goods_sold()
        expenses = analyzer.calculate_total_expenses()
        net_profit = analyzer.calculate_net_profit()
        margin = analyzer.calculate_profit_margin()

        info_frame = ctk.CTkFrame(tab, fg_color=card_fg(), corner_radius=10,
                                  border_width=1, border_color=COLORS["border"])
        info_frame.pack(fill="x", padx=10, pady=10)

        rows = [
            ("Revenue", Helpers.format_currency(revenue, currency), COLORS["success"]),
            ("Cost of Goods Sold", Helpers.format_currency(cogs, currency), COLORS["warning"]),
            ("Expenses", Helpers.format_currency(expenses, currency), COLORS["danger"]),
            ("Net Profit", Helpers.format_currency(net_profit, currency),
             COLORS["success"] if net_profit >= 0 else COLORS["danger"]),
            ("Profit Margin", Helpers.format_percentage(margin),
             COLORS["success"] if margin >= 0 else COLORS["danger"]),
        ]

        for label, value, color in rows:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=4)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=14),
                         text_color=COLORS["text_light"]).pack(side="left", pady=5)
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=color).pack(side="right", pady=5)

    def _build_inventory_report(self, tab):
        inv = self.app.inventory_manager
        currency = self.app.get_currency()

        info_frame = ctk.CTkFrame(tab, fg_color=card_fg(), corner_radius=10,
                                  border_width=1, border_color=COLORS["border"])
        info_frame.pack(fill="x", padx=10, pady=10)

        for label, value in [
            ("Total Products", str(self.app.product_manager.get_total_products())),
            ("In Stock", str(inv.get_in_stock_count())),
            ("Low Stock", str(inv.get_low_stock_count())),
            ("Out of Stock", str(inv.get_out_of_stock_count())),
            ("Total Inventory Value", Helpers.format_currency(inv.get_total_inventory_value(), currency)),
        ]:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=3)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(side="left", pady=5)
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white").pack(side="right", pady=5)

        ctk.CTkLabel(tab, text="Low Stock Items:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        low_df = inv.get_low_stock_items()
        data = []
        if not low_df.empty:
            for _, row in low_df.iterrows():
                data.append({
                    "ProductID": row.get("ProductID", ""),
                    "ProductName": row.get("ProductName", ""),
                    "StockQuantity": row.get("StockQuantity", ""),
                    "ReorderLevel": row.get("ReorderLevel", ""),
                })
        create_table(tab, ["ProductID", "ProductName", "StockQuantity", "ReorderLevel"], data)