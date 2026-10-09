"""
SalesManager - Manages sales data operations.
Handles CRUD operations for sales stored in sales.csv.
"""

import pandas as pd
from utils.file_manager import FileManager
from utils.helpers import Helpers


class SalesManager:
    """Manages sales data using CSV storage."""

    FILENAME = "sales.csv"
    COLUMNS = [
        "SaleID", "Date", "Product", "Customer",
        "Quantity", "UnitPrice", "TotalAmount", "PaymentMethod",
    ]

    def __init__(self, file_manager=None):
        self.file_manager = file_manager or FileManager()
        self.file_manager.create_file_if_missing(
            self.FILENAME, self.COLUMNS
        )

    def get_all_sales(self):
        return self.file_manager.read_csv(self.FILENAME)

    def get_sale_by_id(self, sale_id):
        df = self.get_all_sales()
        if df.empty:
            return None
        matches = df[df["SaleID"].astype(str) == str(sale_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def add_sale(self, date, product, customer, quantity, unit_price, payment_method):
        sale_id = self.file_manager.generate_id(
            self.FILENAME, "SaleID", "SAL"
        )
        total_amount = float(quantity) * float(unit_price)
        row = {
            "SaleID": sale_id,
            "Date": date,
            "Product": product,
            "Customer": customer,
            "Quantity": int(quantity),
            "UnitPrice": float(unit_price),
            "TotalAmount": total_amount,
            "PaymentMethod": payment_method,
        }
        self.file_manager.append_row(self.FILENAME, row, self.COLUMNS)
        return sale_id

    def update_sale(self, sale_id, updated_dict):
        if "Quantity" in updated_dict and "UnitPrice" in updated_dict:
            updated_dict["TotalAmount"] = (
                float(updated_dict["Quantity"]) * float(updated_dict["UnitPrice"])
            )
        return self.file_manager.update_row_by_id(
            self.FILENAME, "SaleID", sale_id, updated_dict
        )

    def delete_sale(self, sale_id):
        return self.file_manager.delete_row_by_id(
            self.FILENAME, "SaleID", sale_id
        )

    def search_sales(self, keyword):
        df = self.get_all_sales()
        if df.empty:
            return df
        mask = (
            df["Product"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Customer"].astype(str).str.contains(keyword, case=False, na=False)
            | df["SaleID"].astype(str).str.contains(keyword, case=False, na=False)
            | df["PaymentMethod"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Date"].astype(str).str.contains(keyword, case=False, na=False)
        )
        return df[mask]

    def filter_by_date_range(self, start_date, end_date):
        df = self.get_all_sales()
        if df.empty:
            return df
        start = Helpers.parse_date(start_date)
        end = Helpers.parse_date(end_date)
        if not start or not end:
            return df
        result = []
        for _, row in df.iterrows():
            sale_date = Helpers.parse_date(row["Date"])
            if sale_date and start <= sale_date <= end:
                result.append(row)
        if result:
            return pd.DataFrame(result)
        return pd.DataFrame(columns=df.columns)

    def filter_by_product(self, product_name):
        df = self.get_all_sales()
        if df.empty:
            return df
        return df[df["Product"].astype(str) == str(product_name)]

    def filter_by_customer(self, customer_name):
        df = self.get_all_sales()
        if df.empty:
            return df
        return df[df["Customer"].astype(str) == str(customer_name)]

    def filter_by_payment(self, payment_method):
        df = self.get_all_sales()
        if df.empty:
            return df
        return df[df["PaymentMethod"].astype(str) == str(payment_method)]

    def get_payment_methods(self):
        return ["Cash", "Card", "Bank Transfer", "Mobile Payment", "Credit"]

    def get_total_sales(self):
        df = self.get_all_sales()
        if df.empty:
            return 0.0
        try:
            return float(df["TotalAmount"].sum())
        except Exception:
            return 0.0

    def get_sales_count(self):
        df = self.get_all_sales()
        return len(df)