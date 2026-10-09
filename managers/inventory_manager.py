"""
InventoryManager - Manages inventory data operations.
Derives inventory status from product data.
"""

import pandas as pd
from utils.helpers import Helpers


class InventoryManager:
    """Manages inventory status derived from product data."""

    def __init__(self, product_manager=None):
        self.product_manager = product_manager

    def get_inventory(self):
        if not self.product_manager:
            return pd.DataFrame()
        df = self.product_manager.get_all_products()
        if df.empty:
            return df
        inventory = df.copy()
        inventory["StockStatus"] = inventory.apply(
            lambda row: Helpers.classify_stock_status(
                row.get("StockQuantity", 0), row.get("ReorderLevel", 0)
            ),
            axis=1,
        )
        return inventory

    def get_low_stock_items(self):
        inv = self.get_inventory()
        if inv.empty:
            return inv
        return inv[inv["StockStatus"] == "LOW STOCK"]

    def get_out_of_stock_items(self):
        inv = self.get_inventory()
        if inv.empty:
            return inv
        return inv[inv["StockStatus"] == "OUT OF STOCK"]

    def get_in_stock_items(self):
        inv = self.get_inventory()
        if inv.empty:
            return inv
        return inv[inv["StockStatus"] == "IN STOCK"]

    def get_low_stock_count(self):
        return len(self.get_low_stock_items())

    def get_out_of_stock_count(self):
        return len(self.get_out_of_stock_items())

    def get_in_stock_count(self):
        return len(self.get_in_stock_items())

    def get_total_inventory_value(self):
        inv = self.get_inventory()
        if inv.empty:
            return 0.0
        try:
            return float(
                (inv["StockQuantity"].astype(float) * inv["CostPrice"].astype(float)).sum()
            )
        except Exception:
            return 0.0

    def search_inventory(self, keyword):
        inv = self.get_inventory()
        if inv.empty:
            return inv
        mask = (
            inv["ProductName"].astype(str).str.contains(keyword, case=False, na=False)
            | inv["Category"].astype(str).str.contains(keyword, case=False, na=False)
            | inv["ProductID"].astype(str).str.contains(keyword, case=False, na=False)
        )
        return inv[mask]

    def restock_product(self, product_id, additional_quantity):
        if not self.product_manager:
            return
        product = self.product_manager.get_product_by_id(product_id)
        if not product:
            return
        current = int(product.get("StockQuantity", 0))
        new_stock = current + int(additional_quantity)
        self.product_manager.update_product(product_id, {"StockQuantity": new_stock})