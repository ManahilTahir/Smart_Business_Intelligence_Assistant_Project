"""
AnalyticsPage - Data analysis page with sales, expense, product, and customer analysis.
"""

import customtkinter as ctk
from gui.components import (create_section_header, create_table, COLORS, card_fg)
from utils.helpers import Helpers
from analysis.calculations import Calculations


class AnalyticsPage:
    """Analytics page showing comprehensive data analysis."""

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

        create_section_header(self.frame, "Analytics",
                               "Comprehensive business data analysis using Pandas and NumPy")

        tabview = ctk.CTkTabview(self.frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=10)

        tabview.add("Sales Analysis")
        tabview.add("Expense Analysis")
        tabview.add("Product Performance")
        tabview.add("Customer Analysis")

        self._build_sales_tab(tabview.tab("Sales Analysis"))
        self._build_expense_tab(tabview.tab("Expense Analysis"))
        self._build_product_tab(tabview.tab("Product Performance"))
        self._build_customer_tab(tabview.tab("Customer Analysis"))

    def _build_sales_tab(self, tab):
        analyzer = self.app.analyzer
        sales = analyzer.get_sales_analysis()
        currency = self.app.get_currency()

        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        stats = [
            ("Total Sales", Helpers.format_currency(sales["total_sales"], currency), 0),
            ("Average Sale", Helpers.format_currency(sales["average_sale"], currency), 1),
            ("Maximum Sale", Helpers.format_currency(sales["max_sale"], currency), 2),
            ("Minimum Sale", Helpers.format_currency(sales["min_sale"], currency), 3),
            ("Total Quantity", str(sales["total_quantity"]), 4),
        ]

        for label, value, idx in stats:
            card = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                border_width=1, border_color=COLORS["border"])
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_light"]).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white").pack(pady=(2, 8))

        ctk.CTkLabel(tab, text="Sales by Product:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        prod_data = []
        if not sales["sales_by_product"].empty:
            for _, row in sales["sales_by_product"].iterrows():
                prod_data.append({"Product": row["Product"], "TotalSales": Helpers.format_currency(row["TotalSales"], currency)})
        create_table(tab, ["Product", "TotalSales"], prod_data)

    def _build_expense_tab(self, tab):
        analyzer = self.app.analyzer
        exp = analyzer.get_expense_analysis()
        currency = self.app.get_currency()

        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        stats = [
            ("Total Expenses", Helpers.format_currency(exp["total_expenses"], currency)),
            ("Average Expense", Helpers.format_currency(exp["average_expense"], currency)),
            ("Highest Expense", Helpers.format_currency(exp["highest_expense"], currency)),
        ]

        for label, value in stats:
            card = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                border_width=1, border_color=COLORS["border"])
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_light"]).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=16, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white").pack(pady=(2, 8))

        ctk.CTkLabel(tab, text="Expense by Category (with percentages):", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        cat_data = []
        if not exp["expense_percentages"].empty:
            for _, row in exp["expense_percentages"].iterrows():
                cat_data.append({
                    "Category": row["Category"],
                    "TotalAmount": Helpers.format_currency(row["TotalAmount"], currency),
                    "Percentage": Helpers.format_percentage(row["Percentage"]),
                })
        create_table(tab, ["Category", "TotalAmount", "Percentage"], cat_data)

    def _build_product_tab(self, tab):
        analyzer = self.app.analyzer
        perf = analyzer.get_product_performance()
        currency = self.app.get_currency()

        summary = analyzer.get_product_performance_summary()
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        for label, count, color in [
            ("High Performers", summary.get("high", 0), COLORS["success"]),
            ("Good Performers", summary.get("good", 0), COLORS["info"]),
            ("Low Performers", summary.get("low", 0), COLORS["warning"]),
        ]:
            card = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                border_width=1, border_color=COLORS["border"])
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_light"]).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=str(count), font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=color).pack(pady=(2, 8))

        ctk.CTkLabel(tab, text="Product Performance Details:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        data = []
        if not perf.empty:
            for _, row in perf.iterrows():
                data.append({
                    "ProductName": row.get("ProductName", ""),
                    "QuantitySold": row.get("QuantitySold", ""),
                    "TotalRevenue": Helpers.format_currency(row.get("TotalRevenue", 0), currency),
                    "TotalProfit": Helpers.format_currency(row.get("TotalProfit", 0), currency),
                    "ProfitMargin": Helpers.format_percentage(row.get("ProfitMargin", 0)),
                    "Performance": row.get("Performance", ""),
                })
        create_table(tab, ["ProductName", "QuantitySold", "TotalRevenue", "TotalProfit", "ProfitMargin", "Performance"], data)

    def _build_customer_tab(self, tab):
        analyzer = self.app.analyzer
        cust = analyzer.get_customer_analysis()
        currency = self.app.get_currency()

        summary = analyzer.get_customer_category_summary()
        stats_frame = ctk.CTkFrame(tab, fg_color="transparent")
        stats_frame.pack(fill="x", padx=10, pady=5)

        for label, count, color in [
            ("VIP", summary.get("vip", 0), "#9B59B6"),
            ("Regular", summary.get("regular", 0), COLORS["info"]),
            ("Occasional", summary.get("occasional", 0), COLORS["text_light"]),
        ]:
            card = ctk.CTkFrame(stats_frame, fg_color=card_fg(), corner_radius=10,
                                border_width=1, border_color=COLORS["border"])
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12),
                         text_color=COLORS["text_light"]).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=str(count), font=ctk.CTkFont(size=22, weight="bold"),
                         text_color=color).pack(pady=(2, 8))

        ctk.CTkLabel(tab, text="Customer Analysis Details:", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(10, 0))
        data = []
        if not cust.empty:
            for _, row in cust.iterrows():
                data.append({
                    "CustomerName": row.get("CustomerName", ""),
                    "City": row.get("City", ""),
                    "TotalSpending": Helpers.format_currency(row.get("TotalSpending", 0), currency),
                    "PurchaseCount": row.get("PurchaseCount", ""),
                    "Category": row.get("Category", ""),
                })
        create_table(tab, ["CustomerName", "City", "TotalSpending", "PurchaseCount", "Category"], data)