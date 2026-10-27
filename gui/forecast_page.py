"""
ForecastPage - ML forecasting page showing predictions for all business areas.
"""

import customtkinter as ctk
from gui.components import (create_section_header, create_button, create_table,
                            create_bar_chart, create_line_chart, COLORS, card_fg)
from utils.helpers import Helpers
from ml.forecaster import Forecaster


class ForecastPage:
    """ML forecasting page with predictions for sales, expenses, profit, products."""

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.forecaster = None
        self.forecast_data = None

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self._build_layout()

    def hide(self):
        self.frame.pack_forget()

    def _build_layout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        create_section_header(self.frame, "ML Forecasting & Predictions",
                               "Machine Learning based business forecasts using Scikit-learn")

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(top_frame, text="Forecast Period:", font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        self.period_combo = ctk.CTkComboBox(top_frame, values=["Next Month (1)", "Next Quarter (3)", "Next 6 Months", "Next Year (12)"],
                                             height=32, width=180)
        self.period_combo.set("Next Quarter (3)")
        self.period_combo.pack(side="left", padx=5)

        create_button(top_frame, "🚀 Generate Forecasts", self._generate_forecasts,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)

        self.status_label = ctk.CTkLabel(self.frame, text="Click 'Generate Forecasts' to run ML predictions",
                                          font=ctk.CTkFont(size=13),
                                          text_color=COLORS["text_light"])
        self.status_label.pack(pady=5)

        self.results_frame = ctk.CTkScrollableFrame(self.frame, fg_color="transparent")
        self.results_frame.pack(fill="both", expand=True, padx=10, pady=5)

    def _get_periods(self):
        choice = self.period_combo.get()
        if "Month" in choice:
            return 1
        if "Quarter" in choice:
            return 3
        if "6 Months" in choice:
            return 6
        if "Year" in choice:
            return 12
        return 3

    def _generate_forecasts(self):
        self.status_label.configure(text="⏳ Running ML forecasts in parallel... Please wait.")
        self.frame.update()

        if self.forecaster is None:
            self.forecaster = Forecaster(
                sales_manager=self.app.sales_manager,
                product_manager=self.app.product_manager,
                customer_manager=self.app.customer_manager,
                expense_manager=self.app.expense_manager,
                inventory_manager=self.app.inventory_manager,
            )

        periods = self._get_periods()

        def progress(msg):
            self.status_label.configure(text=f"⏳ {msg}")
            self.frame.update()

        self.forecast_data = self.forecaster.forecast_all(periods, progress)
        self.status_label.configure(text="✅ Forecasts generated successfully!")
        self._display_results()

    def _display_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        data = self.forecast_data
        currency = self.app.get_currency()

        summary = self.forecaster.get_forecast_summary(self._get_periods())

        kpi_frame = ctk.CTkFrame(self.results_frame, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=10, pady=5)

        kpis = [
            ("Predicted Revenue", Helpers.format_currency(summary.get("total_predicted_revenue", 0), currency), "#3498DB"),
            ("Predicted Expenses", Helpers.format_currency(summary.get("total_predicted_expenses", 0), currency), "#E74C3C"),
            ("Predicted Profit", Helpers.format_currency(summary.get("total_predicted_profit", 0), currency), "#27AE60"),
            ("Top Product", f"{summary.get('top_product', 'N/A')} ({summary.get('top_product_qty', 0)})", "#9B59B6"),
        ]

        for label, value, color in kpis:
            card = ctk.CTkFrame(kpi_frame, fg_color=color, corner_radius=10)
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12, weight="bold"),
                         text_color="#E8E8E8").pack(pady=(10, 0))
            ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=14, weight="bold"),
                         text_color="white", wraplength=180).pack(pady=(2, 10))

        tabview = ctk.CTkTabview(self.results_frame)
        tabview.pack(fill="both", expand=True, padx=10, pady=5)
        tabview.configure(height=500)

        tabview.add("Sales Forecast")
        tabview.add("Expense Forecast")
        tabview.add("Profit Forecast")
        tabview.add("Product Forecast")
        tabview.add("Customer Forecast")
        tabview.add("Inventory Needs")

        self._build_sales_tab(self._wrap_tab(tabview.tab("Sales Forecast")), data.get("sales", {}), currency)
        self._build_expense_tab(self._wrap_tab(tabview.tab("Expense Forecast")), data.get("expenses", {}), currency)
        self._build_profit_tab(self._wrap_tab(tabview.tab("Profit Forecast")), data.get("profit", {}), currency)
        self._build_product_tab(self._wrap_tab(tabview.tab("Product Forecast")), data.get("products", {}), currency)
        self._build_customer_tab(self._wrap_tab(tabview.tab("Customer Forecast")), data.get("customers", {}), currency)
        self._build_inventory_tab(self._wrap_tab(tabview.tab("Inventory Needs")), data.get("inventory", {}), currency)

    def _wrap_tab(self, tab):
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        return scroll

    def _build_sales_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("revenue_forecast", [])
        hist_months = data.get("historical_months", [])
        hist_values = data.get("historical_values", [])

        if hist_months and hist_values:
            all_labels = [m[-2:] for m in hist_months] + [p["month"][-2:] for p in fc]
            all_values = hist_values + [p["predicted"] for p in fc]
            create_line_chart(tab, "Sales: Historical + Forecast", all_labels, all_values, "#2980B9")

        table_data = [{"Month": p["month"], "Predicted Revenue": Helpers.format_currency(p["predicted"], currency)}
                      for p in fc]
        create_table(tab, ["Month", "Predicted Revenue"], table_data)

    def _build_expense_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("expense_forecast", [])
        hist_months = data.get("historical_months", [])
        hist_values = data.get("historical_values", [])

        if hist_months and hist_values:
            all_labels = [m[-2:] for m in hist_months] + [p["month"][-2:] for p in fc]
            all_values = hist_values + [p["predicted"] for p in fc]
            create_line_chart(tab, "Expenses: Historical + Forecast", all_labels, all_values, "#E74C3C")

        table_data = [{"Month": p["month"], "Predicted Expense": Helpers.format_currency(p["predicted"], currency)}
                      for p in fc]
        create_table(tab, ["Month", "Predicted Expense"], table_data)

    def _build_profit_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("profit_forecast", [])
        if fc:
            labels = [p["month"][-2:] for p in fc]
            values = [p["predicted_profit"] for p in fc]
            create_bar_chart(tab, "Predicted Profit by Month", labels, values, "#27AE60")

        table_data = [{
            "Month": p["month"],
            "Pred Revenue": Helpers.format_currency(p["predicted_revenue"], currency),
            "Pred Expenses": Helpers.format_currency(p["predicted_expenses"], currency),
            "Pred Profit": Helpers.format_currency(p["predicted_profit"], currency),
        } for p in fc]
        create_table(tab, ["Month", "Pred Revenue", "Pred Expenses", "Pred Profit"], table_data)

    def _build_product_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("product_forecast", [])
        if fc:
            top10 = fc[:10]
            labels = [p["product"][:12] for p in top10]
            values = [p["predicted_quantity"] for p in top10]
            create_bar_chart(tab, "Top 10 Products - Predicted Demand", labels, values, "multi")

        table_data = [{
            "Product": p["product"],
            "Category": p["category"],
            "CurrentStock": p["current_stock"],
            "PredictedQty": p["predicted_quantity"],
            "RecommendedProd": p["recommended_production"],
        } for p in fc]
        create_table(tab, ["Product", "Category", "CurrentStock", "PredictedQty", "RecommendedProd"], table_data)

    def _build_customer_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("customer_forecast", [])
        table_data = [{
            "Customer": p["customer"],
            "City": p["city"],
            "CurrentSpending": Helpers.format_currency(p["current_spending"], currency),
            "PredictedSpending": Helpers.format_currency(p["predicted_spending"], currency),
        } for p in fc]
        create_table(tab, ["Customer", "City", "CurrentSpending", "PredictedSpending"], table_data)

    def _build_inventory_tab(self, tab, data, currency):
        if "error" in data:
            ctk.CTkLabel(tab, text=data["error"], font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_light"]).pack(pady=20)
            return

        fc = data.get("inventory_forecast", [])
        table_data = [{
            "Product": p["product"],
            "CurrentStock": p["current_stock"],
            "PredictedDemand": p["predicted_demand"],
            "RecommendedProd": p["recommended_production"],
            "Status": p["status"],
        } for p in fc]
        create_table(tab, ["Product", "CurrentStock", "PredictedDemand", "RecommendedProd", "Status"], table_data)