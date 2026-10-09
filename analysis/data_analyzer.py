"""
DataAnalyzer - Main analysis engine using Pandas and NumPy.
Provides business intelligence calculations and insights.
"""

import pandas as pd
import numpy as np
from analysis.calculations import Calculations
from utils.helpers import Helpers


class DataAnalyzer:
    """Performs business data analysis using Pandas and NumPy."""

    def __init__(self, sales_manager=None, product_manager=None,
                 customer_manager=None, expense_manager=None,
                 inventory_manager=None):
        self.sales_manager = sales_manager
        self.product_manager = product_manager
        self.customer_manager = customer_manager
        self.expense_manager = expense_manager
        self.inventory_manager = inventory_manager
        self.vip_threshold = 100000
        self.regular_threshold = 30000

    def set_thresholds(self, vip, regular):
        self.vip_threshold = vip
        self.regular_threshold = regular

    def calculate_total_sales(self):
        if not self.sales_manager:
            return 0.0
        return self.sales_manager.get_total_sales()

    def calculate_total_expenses(self):
        if not self.expense_manager:
            return 0.0
        return self.expense_manager.get_total_expenses()

    def calculate_revenue(self):
        return self.calculate_total_sales()

    def calculate_cost_of_goods_sold(self):
        if not self.sales_manager or not self.product_manager:
            return 0.0
        sales_df = self.sales_manager.get_all_sales()
        if sales_df.empty:
            return 0.0
        total_cost = 0.0
        for _, row in sales_df.iterrows():
            product_name = row.get("Product", "")
            product_id = self.product_manager.get_product_id_by_name(product_name)
            if product_id:
                cost = self.product_manager.get_cost_price_by_id(product_id)
                qty = int(row.get("Quantity", 0))
                total_cost += cost * qty
        return total_cost

    def calculate_net_profit(self):
        revenue = self.calculate_revenue()
        cogs = self.calculate_cost_of_goods_sold()
        expenses = self.calculate_total_expenses()
        return Calculations.net_profit(revenue, cogs, expenses)

    def calculate_profit_margin(self):
        revenue = self.calculate_revenue()
        net_profit = self.calculate_net_profit()
        return Calculations.profit_margin(net_profit, revenue)

    def calculate_total_products(self):
        if not self.product_manager:
            return 0
        return self.product_manager.get_total_products()

    def calculate_total_customers(self):
        if not self.customer_manager:
            return 0
        return self.customer_manager.get_total_customers()

    def calculate_low_stock_count(self):
        if not self.inventory_manager:
            return 0
        return self.inventory_manager.get_low_stock_count()

    def get_dashboard_kpis(self):
        return {
            "total_sales": self.calculate_total_sales(),
            "total_expenses": self.calculate_total_expenses(),
            "net_profit": self.calculate_net_profit(),
            "profit_margin": self.calculate_profit_margin(),
            "total_products": self.calculate_total_products(),
            "total_customers": self.calculate_total_customers(),
            "low_stock_count": self.calculate_low_stock_count(),
        }

    def get_sales_analysis(self):
        result = {
            "total_sales": 0.0, "average_sale": 0.0,
            "max_sale": 0.0, "min_sale": 0.0,
            "total_quantity": 0, "sales_by_product": pd.DataFrame(),
            "sales_by_category": pd.DataFrame(), "sales_by_month": pd.DataFrame(),
        }
        if not self.sales_manager:
            return result
        df = self.sales_manager.get_all_sales()
        if df.empty:
            return result
        amounts = df["TotalAmount"].astype(float)
        result["total_sales"] = Calculations.total(amounts)
        result["average_sale"] = Calculations.mean(amounts)
        result["max_sale"] = Calculations.maximum(amounts)
        result["min_sale"] = Calculations.minimum(amounts)
        result["total_quantity"] = int(df["Quantity"].astype(int).sum())
        result["sales_by_product"] = df.groupby("Product")["TotalAmount"].sum().reset_index()
        result["sales_by_product"].columns = ["Product", "TotalSales"]
        if self.product_manager:
            prod_df = self.product_manager.get_all_products()
            if not prod_df.empty:
                merged = df.merge(prod_df[["ProductName", "Category"]],
                                  left_on="Product", right_on="ProductName", how="left")
                result["sales_by_category"] = merged.groupby("Category")["TotalAmount"].sum().reset_index()
                result["sales_by_category"].columns = ["Category", "TotalSales"]
        df_copy = df.copy()
        df_copy["Month"] = df_copy["Date"].apply(Helpers.get_month_from_date)
        result["sales_by_month"] = df_copy.groupby("Month")["TotalAmount"].sum().reset_index()
        result["sales_by_month"].columns = ["Month", "TotalSales"]
        return result

    def get_expense_analysis(self):
        result = {
            "total_expenses": 0.0, "average_expense": 0.0,
            "highest_expense": 0.0, "expenses_by_category": pd.DataFrame(),
            "monthly_expenses": pd.DataFrame(), "expense_percentages": pd.DataFrame(),
        }
        if not self.expense_manager:
            return result
        df = self.expense_manager.get_all_expenses()
        if df.empty:
            return result
        amounts = df["Amount"].astype(float)
        result["total_expenses"] = Calculations.total(amounts)
        result["average_expense"] = Calculations.mean(amounts)
        result["highest_expense"] = Calculations.maximum(amounts)
        cat_group = df.groupby("Category")["Amount"].sum().reset_index()
        cat_group.columns = ["Category", "TotalAmount"]
        result["expenses_by_category"] = cat_group
        total = result["total_expenses"]
        cat_group["Percentage"] = cat_group["TotalAmount"].apply(
            lambda x: Calculations.percentage(x, total)
        )
        result["expense_percentages"] = cat_group
        df_copy = df.copy()
        df_copy["Month"] = df_copy["Date"].apply(Helpers.get_month_from_date)
        result["monthly_expenses"] = df_copy.groupby("Month")["Amount"].sum().reset_index()
        result["monthly_expenses"].columns = ["Month", "TotalExpenses"]
        return result

    def get_product_performance(self):
        if not self.sales_manager or not self.product_manager:
            return pd.DataFrame()
        sales_df = self.sales_manager.get_all_sales()
        prod_df = self.product_manager.get_all_products()
        if sales_df.empty or prod_df.empty:
            return pd.DataFrame()
        performance = []
        for _, prod in prod_df.iterrows():
            prod_name = prod["ProductName"]
            prod_sales = sales_df[sales_df["Product"].astype(str) == str(prod_name)]
            qty_sold = int(prod_sales["Quantity"].astype(int).sum()) if not prod_sales.empty else 0
            revenue = float(prod_sales["TotalAmount"].astype(float).sum()) if not prod_sales.empty else 0.0
            cost_price = float(prod.get("CostPrice", 0))
            total_cost = cost_price * qty_sold
            total_profit = revenue - total_cost
            margin = Calculations.profit_margin(total_profit, revenue)
            performance.append({
                "ProductID": prod.get("ProductID", ""),
                "ProductName": prod_name,
                "Category": prod.get("Category", ""),
                "QuantitySold": qty_sold,
                "TotalRevenue": revenue,
                "TotalCost": total_cost,
                "TotalProfit": total_profit,
                "ProfitMargin": margin,
            })
        perf_df = pd.DataFrame(performance)
        if perf_df.empty:
            return perf_df
        avg_rev = Calculations.mean(perf_df["TotalRevenue"])
        avg_profit = Calculations.mean(perf_df["TotalProfit"])
        perf_df["Performance"] = perf_df.apply(
            lambda row: Helpers.classify_product_performance(
                row["TotalRevenue"], row["TotalProfit"], avg_rev, avg_profit
            ),
            axis=1,
        )
        return perf_df

    def get_customer_analysis(self):
        if not self.sales_manager or not self.customer_manager:
            return pd.DataFrame()
        sales_df = self.sales_manager.get_all_sales()
        cust_df = self.customer_manager.get_all_customers()
        if sales_df.empty or cust_df.empty:
            return pd.DataFrame()
        spending = sales_df.groupby("Customer").agg(
            TotalSpending=("TotalAmount", "sum"),
            PurchaseCount=("SaleID", "count"),
        ).reset_index()
        result = cust_df.merge(spending, left_on="CustomerName", right_on="Customer", how="left")
        result["TotalSpending"] = result["TotalSpending"].fillna(0)
        result["PurchaseCount"] = result["PurchaseCount"].fillna(0)
        result["Category"] = result["TotalSpending"].apply(
            lambda x: Helpers.classify_customer_category(
                x, self.vip_threshold, self.regular_threshold
            )
        )
        cols = ["CustomerID", "CustomerName", "City", "TotalSpending", "PurchaseCount", "Category"]
        cols = [c for c in cols if c in result.columns]
        return result[cols]

    def get_best_selling_product(self):
        perf = self.get_product_performance()
        if perf.empty:
            return None
        best = perf.loc[perf["QuantitySold"].idxmax()]
        return best.to_dict()

    def get_highest_spending_customer(self):
        cust_analysis = self.get_customer_analysis()
        if cust_analysis.empty:
            return None
        top = cust_analysis.loc[cust_analysis["TotalSpending"].idxmax()]
        return top.to_dict()

    def get_highest_expense_category(self):
        exp_analysis = self.get_expense_analysis()
        cat_df = exp_analysis["expenses_by_category"]
        if cat_df.empty:
            return None
        top = cat_df.loc[cat_df["TotalAmount"].idxmax()]
        return top.to_dict()

    def get_business_insights(self):
        insights = []
        kpis = self.get_dashboard_kpis()
        sales_analysis = self.get_sales_analysis()
        expense_analysis = self.get_expense_analysis()

        best_product = self.get_best_selling_product()
        if best_product and best_product.get("QuantitySold", 0) > 0:
            insights.append(
                f"{best_product['ProductName']} is currently the best-selling product "
                f"with {int(best_product['QuantitySold'])} units sold."
            )

        highest_exp = self.get_highest_expense_category()
        if highest_exp:
            insights.append(
                f"{highest_exp['Category']} is the highest expense category."
            )

        low_stock = kpis["low_stock_count"]
        if low_stock > 0:
            insights.append(f"{low_stock} products are currently below their reorder level.")

        margin = kpis["profit_margin"]
        if margin > 0:
            insights.append(f"Profit margin is currently {margin:.1f}%.")
        elif margin < 0:
            insights.append(f"The business is operating at a loss with a {margin:.1f}% margin.")

        top_customer = self.get_highest_spending_customer()
        if top_customer and top_customer.get("TotalSpending", 0) > 0:
            insights.append(
                f"{top_customer['CustomerName']} has the highest total purchase value."
            )

        monthly_sales = sales_analysis["sales_by_month"]
        if not monthly_sales.empty and len(monthly_sales) >= 2:
            monthly_sales = monthly_sales.sort_values("Month")
            last = monthly_sales.iloc[-1]["TotalSales"]
            prev = monthly_sales.iloc[-2]["TotalSales"]
            change = Calculations.percent_change(prev, last)
            if change > 0:
                insights.append(f"Sales increased by {change:.1f}% compared with the previous month.")
            elif change < 0:
                insights.append(f"Sales decreased by {abs(change):.1f}% compared with the previous month.")

        monthly_exp = expense_analysis["monthly_expenses"]
        if not monthly_exp.empty and len(monthly_exp) >= 2:
            monthly_exp = monthly_exp.sort_values("Month")
            last = monthly_exp.iloc[-1]["TotalExpenses"]
            prev = monthly_exp.iloc[-2]["TotalExpenses"]
            change = Calculations.percent_change(prev, last)
            if change > 0:
                insights.append(f"Expenses increased by {change:.1f}% compared with the previous month.")
            elif change < 0:
                insights.append(f"Expenses decreased by {abs(change):.1f}% compared with the previous month.")

        return insights

    def get_product_performance_summary(self):
        perf = self.get_product_performance()
        if perf.empty:
            return {}
        return {
            "high": len(perf[perf["Performance"] == "High Performer"]),
            "good": len(perf[perf["Performance"] == "Good Performer"]),
            "low": len(perf[perf["Performance"] == "Low Performer"]),
        }

    def get_customer_category_summary(self):
        cust = self.get_customer_analysis()
        if cust.empty:
            return {}
        return {
            "vip": len(cust[cust["Category"] == "VIP"]),
            "regular": len(cust[cust["Category"] == "Regular"]),
            "occasional": len(cust[cust["Category"] == "Occasional"]),
        }