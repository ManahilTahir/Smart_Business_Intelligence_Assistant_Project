"""
Forecaster - ML forecasting engine using Scikit-learn.
Predicts sales, revenue, expenses, and profit for future periods.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from ml.parallel import cached, run_parallel, clear_cache


class Forecaster:
    """ML-based forecasting for business data using Scikit-learn."""

    def __init__(self, sales_manager=None, product_manager=None,
                 customer_manager=None, expense_manager=None,
                 inventory_manager=None):
        self.sales_manager = sales_manager
        self.product_manager = product_manager
        self.customer_manager = customer_manager
        self.expense_manager = expense_manager
        self.inventory_manager = inventory_manager

    def _prepare_monthly_data(self, df, date_col, value_col):
        if df.empty or date_col not in df.columns or value_col not in df.columns:
            return pd.DataFrame()
        df = df.copy()
        df["Month"] = df[date_col].astype(str).str[:7]
        monthly = df.groupby("Month")[value_col].sum().reset_index()
        monthly = monthly.sort_values("Month")
        monthly["MonthNum"] = range(len(monthly))
        return monthly

    def _forecast_series(self, monthly_df, periods, model_type="linear"):
        if monthly_df.empty or len(monthly_df) < 2:
            return []
        X = monthly_df["MonthNum"].values.reshape(-1, 1)
        y = monthly_df[monthly_df.columns[1]].values

        if model_type == "rf" and len(monthly_df) >= 5:
            model = RandomForestRegressor(n_estimators=50, random_state=42)
        else:
            model = LinearRegression()

        model.fit(X, y)
        last_num = monthly_df["MonthNum"].iloc[-1]
        future_X = np.array([[last_num + i + 1] for i in range(periods)])
        predictions = model.predict(future_X)

        last_month = monthly_df["Month"].iloc[-1]
        future_months = []
        year, month = int(last_month[:4]), int(last_month[5:7])
        for i in range(periods):
            month += 1
            if month > 12:
                month = 1
                year += 1
            future_months.append(f"{year}-{month:02d}")

        return [{"month": future_months[i], "predicted": max(0, round(predictions[i], 2))}
                for i in range(periods)]

    @cached("sales_forecast")
    def forecast_sales(self, periods=3):
        if not self.sales_manager:
            return {"error": "No sales data available"}
        df = self.sales_manager.get_all_sales()
        if df.empty:
            return {"error": "No sales records found"}
        monthly = self._prepare_monthly_data(df, "Date", "TotalAmount")
        predictions = self._forecast_series(monthly, periods)
        qty_monthly = self._prepare_monthly_data(df, "Date", "Quantity")
        qty_predictions = self._forecast_series(qty_monthly, periods)
        return {
            "revenue_forecast": predictions,
            "quantity_forecast": qty_predictions,
            "historical_months": monthly["Month"].tolist() if not monthly.empty else [],
            "historical_values": monthly[monthly.columns[1]].tolist() if not monthly.empty else [],
        }

    @cached("expense_forecast")
    def forecast_expenses(self, periods=3):
        if not self.expense_manager:
            return {"error": "No expense data available"}
        df = self.expense_manager.get_all_expenses()
        if df.empty:
            return {"error": "No expense records found"}
        monthly = self._prepare_monthly_data(df, "Date", "Amount")
        predictions = self._forecast_series(monthly, periods)
        return {
            "expense_forecast": predictions,
            "historical_months": monthly["Month"].tolist() if not monthly.empty else [],
            "historical_values": monthly[monthly.columns[1]].tolist() if not monthly.empty else [],
        }

    @cached("profit_forecast")
    def forecast_profit(self, periods=3):
        sales_fc = self.forecast_sales(periods)
        exp_fc = self.forecast_expenses(periods)
        if "error" in sales_fc or "error" in exp_fc:
            return {"error": "Insufficient data for profit forecast"}
        profit_predictions = []
        for s, e in zip(sales_fc["revenue_forecast"], exp_fc["expense_forecast"]):
            profit_predictions.append({
                "month": s["month"],
                "predicted_revenue": s["predicted"],
                "predicted_expenses": e["predicted"],
                "predicted_profit": round(s["predicted"] - e["predicted"], 2),
            })
        return {"profit_forecast": profit_predictions}

    @cached("product_forecast")
    def forecast_product_sales(self, periods=3):
        if not self.sales_manager or not self.product_manager:
            return {"error": "No data available"}
        sales_df = self.sales_manager.get_all_sales()
        prod_df = self.product_manager.get_all_products()
        if sales_df.empty or prod_df.empty:
            return {"error": "Insufficient data"}

        results = []
        for _, prod in prod_df.iterrows():
            prod_name = prod["ProductName"]
            prod_sales = sales_df[sales_df["Product"].astype(str) == str(prod_name)]
            if prod_sales.empty:
                results.append({
                    "product": prod_name,
                    "category": prod.get("Category", ""),
                    "current_stock": int(prod.get("StockQuantity", 0)),
                    "reorder_level": int(prod.get("ReorderLevel", 0)),
                    "predicted_quantity": 0,
                    "recommendation": "No sales history",
                })
                continue
            monthly = self._prepare_monthly_data(prod_sales, "Date", "Quantity")
            predictions = self._forecast_series(monthly, periods)
            total_predicted = sum(p["predicted"] for p in predictions) if predictions else 0

            current_stock = int(prod.get("StockQuantity", 0))
            reorder_level = int(prod.get("ReorderLevel", 0))
            safety_stock = reorder_level
            recommended = max(0, int(total_predicted) - current_stock + safety_stock)

            results.append({
                "product": prod_name,
                "category": prod.get("Category", ""),
                "current_stock": current_stock,
                "reorder_level": reorder_level,
                "predicted_quantity": int(total_predicted),
                "recommended_production": recommended,
            })

        results.sort(key=lambda x: x["predicted_quantity"], reverse=True)
        return {"product_forecast": results}

    @cached("customer_forecast")
    def forecast_customer_spending(self, periods=3):
        if not self.sales_manager or not self.customer_manager:
            return {"error": "No data available"}
        sales_df = self.sales_manager.get_all_sales()
        cust_df = self.customer_manager.get_all_customers()
        if sales_df.empty or cust_df.empty:
            return {"error": "Insufficient data"}

        results = []
        for _, cust in cust_df.iterrows():
            cust_name = cust["CustomerName"]
            cust_sales = sales_df[sales_df["Customer"].astype(str) == str(cust_name)]
            if cust_sales.empty:
                continue
            monthly = self._prepare_monthly_data(cust_sales, "Date", "TotalAmount")
            predictions = self._forecast_series(monthly, periods)
            total_predicted = sum(p["predicted"] for p in predictions) if predictions else 0
            results.append({
                "customer": cust_name,
                "city": cust.get("City", ""),
                "current_spending": float(cust.get("TotalPurchases", 0)),
                "predicted_spending": round(total_predicted, 2),
            })

        results.sort(key=lambda x: x["predicted_spending"], reverse=True)
        return {"customer_forecast": results[:15]}

    @cached("inventory_forecast")
    def forecast_inventory_needs(self, periods=3):
        prod_fc = self.forecast_product_sales(periods)
        if "error" in prod_fc:
            return prod_fc
        results = []
        for item in prod_fc["product_forecast"]:
            status = "OK"
            if item["current_stock"] <= item["reorder_level"]:
                status = "NEEDS RESTOCK"
            if item["predicted_quantity"] > item["current_stock"]:
                status = "INSUFFICIENT FOR FORECAST"
            results.append({
                "product": item["product"],
                "current_stock": item["current_stock"],
                "predicted_demand": item["predicted_quantity"],
                "recommended_production": item["recommended_production"],
                "status": status,
            })
        return {"inventory_forecast": results}

    def forecast_all(self, periods=3, progress_callback=None):
        clear_cache()
        tasks = {
            "sales": lambda: self.forecast_sales(periods),
            "expenses": lambda: self.forecast_expenses(periods),
            "profit": lambda: self.forecast_profit(periods),
            "products": lambda: self.forecast_product_sales(periods),
            "customers": lambda: self.forecast_customer_spending(periods),
            "inventory": lambda: self.forecast_inventory_needs(periods),
        }
        if progress_callback:
            progress_callback("Running parallel forecasts...")
        results = run_parallel(tasks, max_workers=4)
        if progress_callback:
            progress_callback("Done!")
        return results

    def get_forecast_summary(self, periods=3):
        all_fc = self.forecast_all(periods)
        summary = {}
        if "sales" in all_fc and "revenue_forecast" in all_fc["sales"]:
            summary["total_predicted_revenue"] = sum(
                p["predicted"] for p in all_fc["sales"]["revenue_forecast"]
            )
        if "expenses" in all_fc and "expense_forecast" in all_fc["expenses"]:
            summary["total_predicted_expenses"] = sum(
                p["predicted"] for p in all_fc["expenses"]["expense_forecast"]
            )
        if "profit" in all_fc and "profit_forecast" in all_fc["profit"]:
            summary["total_predicted_profit"] = sum(
                p["predicted_profit"] for p in all_fc["profit"]["profit_forecast"]
            )
        if "products" in all_fc and "product_forecast" in all_fc["products"]:
            prods = all_fc["products"]["product_forecast"]
            if prods:
                summary["top_product"] = prods[0]["product"]
                summary["top_product_qty"] = prods[0]["predicted_quantity"]
                summary["low_product"] = prods[-1]["product"]
                summary["low_product_qty"] = prods[-1]["predicted_quantity"]
        return summary