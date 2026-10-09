"""
Dashboard - Main dashboard page showing KPI cards and business insights.
"""

import customtkinter as ctk
from gui.components import (create_card, create_section_header, COLORS, card_fg)
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

        row2 = ctk.CTkFrame(cards_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        for i in range(4, 7):
            title, value, icon, idx = cards[i]
            card = create_card(row2, title, value, icon, idx)
            card.pack(side="left", expand=True, fill="both", padx=8, pady=5)
            card.configure(height=130)

        self._show_insights()

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