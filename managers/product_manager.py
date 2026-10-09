"""
ProductManager - Manages product data operations.
Handles CRUD operations for products stored in products.csv.
"""

import pandas as pd
from utils.file_manager import FileManager


class ProductManager:
    """Manages product data using CSV storage."""

    FILENAME = "products.csv"
    COLUMNS = [
        "ProductID", "ProductName", "Category", "CostPrice",
        "SellingPrice", "StockQuantity", "ReorderLevel",
    ]

    def __init__(self, file_manager=None):
        self.file_manager = file_manager or FileManager()
        self.file_manager.create_file_if_missing(
            self.FILENAME, self.COLUMNS
        )

    def get_all_products(self):
        return self.file_manager.read_csv(self.FILENAME)

    def get_product_by_id(self, product_id):
        df = self.get_all_products()
        if df.empty:
            return None
        matches = df[df["ProductID"].astype(str) == str(product_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def add_product(self, name, category, cost_price, selling_price, stock, reorder):
        product_id = self.file_manager.generate_id(
            self.FILENAME, "ProductID", "PRD"
        )
        row = {
            "ProductID": product_id,
            "ProductName": name,
            "Category": category,
            "CostPrice": float(cost_price),
            "SellingPrice": float(selling_price),
            "StockQuantity": int(stock),
            "ReorderLevel": int(reorder),
        }
        self.file_manager.append_row(self.FILENAME, row, self.COLUMNS)
        return product_id

    def update_product(self, product_id, updated_dict):
        return self.file_manager.update_row_by_id(
            self.FILENAME, "ProductID", product_id, updated_dict
        )

    def delete_product(self, product_id):
        return self.file_manager.delete_row_by_id(
            self.FILENAME, "ProductID", product_id
        )

    def search_products(self, keyword):
        df = self.get_all_products()
        if df.empty:
            return df
        mask = (
            df["ProductName"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Category"].astype(str).str.contains(keyword, case=False, na=False)
            | df["ProductID"].astype(str).str.contains(keyword, case=False, na=False)
        )
        return df[mask]

    def filter_by_category(self, category):
        df = self.get_all_products()
        if df.empty or category == "All":
            return df
        return df[df["Category"].astype(str) == category]

    def get_categories(self):
        df = self.get_all_products()
        if df.empty:
            return []
        return sorted(df["Category"].dropna().unique().tolist())

    def get_product_names(self):
        df = self.get_all_products()
        if df.empty:
            return []
        return df["ProductName"].tolist()

    def get_product_name_by_id(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            return product.get("ProductName", "")
        return ""

    def get_product_id_by_name(self, product_name):
        df = self.get_all_products()
        if df.empty:
            return ""
        matches = df[df["ProductName"].astype(str) == str(product_name)]
        if matches.empty:
            return ""
        return matches.iloc[0]["ProductID"]

    def get_selling_price_by_name(self, product_name):
        df = self.get_all_products()
        if df.empty:
            return 0.0
        matches = df[df["ProductName"].astype(str) == str(product_name)]
        if matches.empty:
            return 0.0
        try:
            return float(matches.iloc[0]["SellingPrice"])
        except (ValueError, TypeError):
            return 0.0

    def get_cost_price_by_id(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            try:
                return float(product.get("CostPrice", 0))
            except (ValueError, TypeError):
                return 0.0
        return 0.0

    def reduce_stock(self, product_name, quantity):
        df = self.get_all_products()
        if df.empty:
            return
        mask = df["ProductName"].astype(str) == str(product_name)
        if mask.any():
            current = int(df.loc[mask, "StockQuantity"].iloc[0])
            df.loc[mask, "StockQuantity"] = max(0, current - int(quantity))
            self.file_manager.write_csv(self.FILENAME, df)

    def get_low_stock_products(self):
        df = self.get_all_products()
        if df.empty:
            return df
        try:
            return df[df["StockQuantity"].astype(int) <= df["ReorderLevel"].astype(int)]
        except Exception:
            return pd.DataFrame()

    def get_out_of_stock_products(self):
        df = self.get_all_products()
        if df.empty:
            return df
        try:
            return df[df["StockQuantity"].astype(int) == 0]
        except Exception:
            return pd.DataFrame()

    def get_total_products(self):
        df = self.get_all_products()
        return len(df)