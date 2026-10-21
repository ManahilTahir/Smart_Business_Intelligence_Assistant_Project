"""
Dashboard - Main dashboard page showing KPI cards and business insights.
"""

import customtkinter as ctk
from gui.components import (create_card, create_section_header, COLORS, card_fg,
                            create_bar_chart, create_line_chart, create_pie_chart)
from utils.helpers import Helpers


class Dashboard:
    """Dashboard page with KPI cards and business insights."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.currency = "PKR"

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.refresh()

    def hide(self):
        self.frame.pack_forget()

    def refresh(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.currency = self.app.get_currency()
        analyzer = self.app.analyzer
        kpis = analyzer.get_dashboard_kpis()

        create_section_header(self.frame, "BusinessHub Dashboard",
                               f"Business Intelligence & Analytics - {self.app.get_business_name()}")

        cards_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        cards_frame.pack(fill="x", padx=20, pady=10)

        cards = [
            ("Total Sales", Helpers.format_currency(kpis["total_sales"], self.currency), "💰", 0),
            ("Total Expenses", Helpers.format_currency(kpis["total_expenses"], self.currency), "📉", 1),
            ("Net Profit", Helpers.format_currency(kpis["net_profit"], self.currency), "📈", 2),
            ("Profit Margin", Helpers.format_percentage(kpis["profit_margin"]), "🎯", 3),
            ("Total Products", str(kpis["total_products"]), "📦", 4),
            ("Total Customers", str(kpis["total_customers"]), "👥", 5),
            ("Low Stock Items", str(kpis["low_stock_count"]), "⚠️", 6),
        ]

        row1 = ctk.CTkFrame(cards_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        for i in range(4):
            title, value, icon, idx = cards[i]
            card = create_card(row1, title, value, icon, idx)
            card.pack(side="left", expand=True, fill="both", padx=8, pady=5)
            card.configure(height=130)
            card.bind("<Button-1>", lambda e, t=title: self._show_card_charts(t))

        row2 = ctk.CTkFrame(cards_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        for i in range(4, 7):
            title, value, icon, idx = cards[i]
            card = create_card(row2, title, value, icon, idx)
            card.pack(side="left", expand=True, fill="both", padx=8, pady=5)
            card.configure(height=130)
            card.bind("<Button-1>", lambda e, t=title: self._show_card_charts(t))

        self._show_charts()
        self._show_insights()

    def _show_charts(self):
        analyzer = self.app.analyzer
        sales_analysis = analyzer.get_sales_analysis()
        expense_analysis = analyzer.get_expense_analysis()

        charts_row1 = ctk.CTkFrame(self.frame, fg_color="transparent")
        charts_row1.pack(fill="x", padx=20, pady=5)

        monthly_sales = sales_analysis["sales_by_month"]
        if not monthly_sales.empty:
            monthly_sales = monthly_sales.sort_values("Month")
            labels = [m[-2:] for m in monthly_sales["Month"].tolist()]
            values = monthly_sales["TotalSales"].tolist()
        else:
            labels, values = [], []
        create_line_chart(charts_row1, "Monthly Sales Trend", labels, values, "#2980B9")

        exp_cat = expense_analysis["expenses_by_category"]
        if not exp_cat.empty:
            labels = exp_cat["Category"].tolist()
            values = exp_cat["TotalAmount"].tolist()
        else:
            labels, values = [], []
        create_bar_chart(charts_row1, "Expenses by Category", labels, values, "multi")

        charts_row2 = ctk.CTkFrame(self.frame, fg_color="transparent")
        charts_row2.pack(fill="x", padx=20, pady=5)

        sales_by_prod = sales_analysis["sales_by_product"]
        if not sales_by_prod.empty:
            top_prods = sales_by_prod.sort_values("TotalSales", ascending=False).head(8)
            labels = top_prods["Product"].tolist()
            values = top_prods["TotalSales"].tolist()
        else:
            labels, values = [], []
        create_bar_chart(charts_row2, "Top Products by Sales", labels, values, "multi")

        monthly_exp = expense_analysis["monthly_expenses"]
        if not monthly_exp.empty:
            monthly_exp = monthly_exp.sort_values("Month")
            labels = [m[-2:] for m in monthly_exp["Month"].tolist()]
            values = monthly_exp["TotalExpenses"].tolist()
        else:
            labels, values = [], []
        create_line_chart(charts_row2, "Monthly Expense Trend", labels, values, "#E74C3C")

    def _show_insights(self):
        insights_frame = ctk.CTkFrame(self.frame, fg_color=card_fg(), corner_radius=12,
                                       border_width=1, border_color=COLORS["border"])
        insights_frame.pack(fill="both", expand=True, padx=20, pady=10)

        header = ctk.CTkLabel(insights_frame, text="📊 Data-Based Business Insights",
                              font=ctk.CTkFont(size=18, weight="bold"),
                              text_color=COLORS["primary"])
        header.pack(anchor="w", padx=15, pady=(15, 5))

        sub = ctk.CTkLabel(insights_frame, text="Generated from actual business data using rule-based analysis",
                           font=ctk.CTkFont(size=12),
                           text_color=COLORS["text_light"])
        sub.pack(anchor="w", padx=15, pady=(0, 10))

        insights = self.app.analyzer.get_business_insights()
        if not insights:
            no_data = ctk.CTkLabel(insights_frame, text="No insights available. Add more data to generate insights.",
                                   font=ctk.CTkFont(size=13),
                                   text_color=COLORS["text_light"])
            no_data.pack(pady=20)
            return

        scroll = ctk.CTkScrollableFrame(insights_frame, fg_color=card_fg())
        scroll.pack(fill="both", expand=True, padx=10, pady=(0, 15))

        for i, insight in enumerate(insights):
            insight_frame = ctk.CTkFrame(scroll, fg_color=card_fg(), corner_radius=8,
                                         border_width=1, border_color=COLORS["border"])
            insight_frame.pack(fill="x", pady=3, padx=5)

            num_label = ctk.CTkLabel(insight_frame, text=f"{i+1}.",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     text_color=COLORS["primary"], width=30)
            num_label.pack(side="left", padx=(10, 5), pady=8)

            text_label = ctk.CTkLabel(insight_frame, text=insight,
                                      font=ctk.CTkFont(size=13),
                                      text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white",
                                      wraplength=800, anchor="w")
            text_label.pack(side="left", fill="x", expand=True, padx=5, pady=8)
    def _show_card_charts(self, card_title):
        analyzer = self.app.analyzer
        sales_analysis = analyzer.get_sales_analysis()
        expense_analysis = analyzer.get_expense_analysis()

        dialog = ctk.CTkToplevel(self.frame)
        dialog.title(f"{card_title} - Detailed Analysis")
        dialog.geometry("900x600")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=f"📊 {card_title} Analysis",
                     font=ctk.CTkFont(size=22, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(15, 5))

        scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        if card_title == "Total Sales":
            ms = sales_analysis["sales_by_month"]
            if not ms.empty:
                ms = ms.sort_values("Month")
                labels = [m[-2:] for m in ms["Month"].tolist()]
                values = ms["TotalSales"].tolist()
            else:
                labels, values = [], []
            create_line_chart(scroll, "Monthly Sales Trend", labels, values, "#2980B9")

            sp = sales_analysis["sales_by_product"]
            if not sp.empty:
                sp = sp.sort_values("TotalSales", ascending=False).head(10)
                labels = sp["Product"].tolist()
                values = sp["TotalSales"].tolist()
            else:
                labels, values = [], []
            create_bar_chart(scroll, "Sales by Product", labels, values, "multi")

            sc = sales_analysis["sales_by_category"]
            if not sc.empty:
                labels = sc["Category"].tolist()
                values = sc["TotalSales"].tolist()
            else:
                labels, values = [], []
            create_pie_chart(scroll, "Sales by Category", labels, values)

        elif card_title == "Total Expenses":
            me = expense_analysis["monthly_expenses"]
            if not me.empty:
                me = me.sort_values("Month")
                labels = [m[-2:] for m in me["Month"].tolist()]
                values = me["TotalExpenses"].tolist()
            else:
                labels, values = [], []
            create_line_chart(scroll, "Monthly Expense Trend", labels, values, "#E74C3C")

            ec = expense_analysis["expenses_by_category"]
            if not ec.empty:
                labels = ec["Category"].tolist()
                values = ec["TotalAmount"].tolist()
            else:
                labels, values = [], []
            create_bar_chart(scroll, "Expenses by Category", labels, values, "multi")
            create_pie_chart(scroll, "Expense Distribution", labels, values)

        elif card_title == "Net Profit":
            ms = sales_analysis["sales_by_month"]
            me = expense_analysis["monthly_expenses"]
            if not ms.empty and not me.empty:
                ms = ms.sort_values("Month")
                me = me.sort_values("Month")
                labels = [m[-2:] for m in ms["Month"].tolist()]
                sales_vals = ms["TotalSales"].tolist()
                exp_vals = [me[me["Month"] == m]["TotalExpenses"].iloc[0] if not me[me["Month"] == m].empty else 0 for m in ms["Month"]]
                profit_vals = [s - e for s, e in zip(sales_vals, exp_vals)]
            else:
                labels, profit_vals = [], []
            create_line_chart(scroll, "Monthly Profit Trend", labels, profit_vals, "#27AE60")
            create_bar_chart(scroll, "Monthly Profit", labels, profit_vals, "#27AE60")

        elif card_title == "Profit Margin":
            ms = sales_analysis["sales_by_month"]
            me = expense_analysis["monthly_expenses"]
            if not ms.empty and not me.empty:
                ms = ms.sort_values("Month")
                me = me.sort_values("Month")
                labels = [m[-2:] for m in ms["Month"].tolist()]
                margins = []
                for m in ms["Month"]:
                    s = ms[ms["Month"] == m]["TotalSales"].iloc[0] if not ms[ms["Month"] == m].empty else 0
                    e = me[me["Month"] == m]["TotalExpenses"].iloc[0] if not me[me["Month"] == m].empty else 0
                    margins.append((s - e) / s * 100 if s > 0 else 0)
            else:
                labels, margins = [], []
            create_line_chart(scroll, "Monthly Profit Margin %", labels, margins, "#9B59B6")
            create_bar_chart(scroll, "Profit Margin by Month", labels, margins, "multi")

        elif card_title == "Total Products":
            perf = analyzer.get_product_performance()
            if not perf.empty:
                perf = perf.sort_values("QuantitySold", ascending=False).head(10)
                labels = perf["ProductName"].tolist()
                values = perf["QuantitySold"].tolist()
            else:
                labels, values = [], []
            create_bar_chart(scroll, "Products by Quantity Sold", labels, values, "multi")

            if not perf.empty:
                labels = perf["ProductName"].tolist()
                values = perf["TotalRevenue"].tolist()
            else:
                labels, values = [], []
            create_pie_chart(scroll, "Revenue Distribution", labels, values)

        elif card_title == "Total Customers":
            cust = analyzer.get_customer_analysis()
            if not cust.empty:
                by_city = cust.groupby("City")["TotalSpending"].sum().reset_index()
                labels = by_city["City"].tolist()
                values = by_city["TotalSpending"].tolist()
            else:
                labels, values = [], []
            create_bar_chart(scroll, "Customer Spending by City", labels, values, "multi")
            create_pie_chart(scroll, "Spending Distribution by City", labels, values)

        elif card_title == "Low Stock Items":
            inv = self.app.inventory_manager
            low_df = inv.get_low_stock_items()
            out_df = inv.get_out_of_stock_items()
            in_df = inv.get_in_stock_items()
            labels = ["In Stock", "Low Stock", "Out of Stock"]
            values = [len(in_df), len(low_df), len(out_df)]
            create_pie_chart(scroll, "Stock Status Distribution", labels, values)
            create_bar_chart(scroll, "Stock Status Count", labels, values, "multi")