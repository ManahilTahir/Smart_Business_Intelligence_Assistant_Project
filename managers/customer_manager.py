"""
CustomerManager - Manages customer data operations.
Handles CRUD operations for customers stored in customers.csv.
"""

import pandas as pd
from utils.file_manager import FileManager


class CustomerManager:
    """Manages customer data using CSV storage."""

    FILENAME = "customers.csv"
    COLUMNS = [
        "CustomerID", "CustomerName", "Phone", "Email",
        "City", "TotalPurchases",
    ]

    def __init__(self, file_manager=None):
        self.file_manager = file_manager or FileManager()
        self.file_manager.create_file_if_missing(
            self.FILENAME, self.COLUMNS
        )

    def get_all_customers(self):
        return self.file_manager.read_csv(self.FILENAME)

    def get_customer_by_id(self, customer_id):
        df = self.get_all_customers()
        if df.empty:
            return None
        matches = df[df["CustomerID"].astype(str) == str(customer_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def add_customer(self, name, phone, email, city):
        customer_id = self.file_manager.generate_id(
            self.FILENAME, "CustomerID", "CUST"
        )
        row = {
            "CustomerID": customer_id,
            "CustomerName": name,
            "Phone": phone,
            "Email": email,
            "City": city,
            "TotalPurchases": 0.0,
        }
        self.file_manager.append_row(self.FILENAME, row, self.COLUMNS)
        return customer_id

    def update_customer(self, customer_id, updated_dict):
        return self.file_manager.update_row_by_id(
            self.FILENAME, "CustomerID", customer_id, updated_dict
        )

    def delete_customer(self, customer_id):
        return self.file_manager.delete_row_by_id(
            self.FILENAME, "CustomerID", customer_id
        )

    def search_customers(self, keyword):
        df = self.get_all_customers()
        if df.empty:
            return df
        mask = (
            df["CustomerName"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Phone"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Email"].astype(str).str.contains(keyword, case=False, na=False)
            | df["City"].astype(str).str.contains(keyword, case=False, na=False)
            | df["CustomerID"].astype(str).str.contains(keyword, case=False, na=False)
        )
        return df[mask]

    def get_customer_names(self):
        df = self.get_all_customers()
        if df.empty:
            return []
        return df["CustomerName"].tolist()

    def get_customer_id_by_name(self, customer_name):
        df = self.get_all_customers()
        if df.empty:
            return ""
        matches = df[df["CustomerName"].astype(str) == str(customer_name)]
        if matches.empty:
            return ""
        return matches.iloc[0]["CustomerID"]

    def update_total_purchases(self, customer_id, amount, replace=False):
        df = self.get_all_customers()
        if df.empty:
            return
        mask = df["CustomerID"].astype(str) == str(customer_id)
        if mask.any():
            if replace:
                df.loc[mask, "TotalPurchases"] = float(amount)
            else:
                current = float(df.loc[mask, "TotalPurchases"].iloc[0])
                df.loc[mask, "TotalPurchases"] = current + float(amount)
            self.file_manager.write_csv(self.FILENAME, df)

    def get_total_customers(self):
        df = self.get_all_customers()
        return len(df)

    def get_cities(self):
        df = self.get_all_customers()
        if df.empty:
            return []
        return sorted(df["City"].dropna().unique().tolist())