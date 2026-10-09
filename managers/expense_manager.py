"""
ExpenseManager - Manages expense data operations.
Handles CRUD operations for expenses stored in expenses.csv.
"""

import pandas as pd
from utils.file_manager import FileManager
from utils.helpers import Helpers


class ExpenseManager:
    """Manages expense data using CSV storage."""

    FILENAME = "expenses.csv"
    COLUMNS = [
        "ExpenseID", "Date", "Category", "Description", "Amount",
    ]

    CATEGORIES = [
        "Rent", "Salary", "Utilities", "Marketing",
        "Transportation", "Inventory", "Technology", "Other",
    ]

    def __init__(self, file_manager=None):
        self.file_manager = file_manager or FileManager()
        self.file_manager.create_file_if_missing(
            self.FILENAME, self.COLUMNS
        )

    def get_all_expenses(self):
        return self.file_manager.read_csv(self.FILENAME)

    def get_expense_by_id(self, expense_id):
        df = self.get_all_expenses()
        if df.empty:
            return None
        matches = df[df["ExpenseID"].astype(str) == str(expense_id)]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def add_expense(self, date, category, description, amount):
        expense_id = self.file_manager.generate_id(
            self.FILENAME, "ExpenseID", "EXP"
        )
        row = {
            "ExpenseID": expense_id,
            "Date": date,
            "Category": category,
            "Description": description,
            "Amount": float(amount),
        }
        self.file_manager.append_row(self.FILENAME, row, self.COLUMNS)
        return expense_id

    def update_expense(self, expense_id, updated_dict):
        return self.file_manager.update_row_by_id(
            self.FILENAME, "ExpenseID", expense_id, updated_dict
        )

    def delete_expense(self, expense_id):
        return self.file_manager.delete_row_by_id(
            self.FILENAME, "ExpenseID", expense_id
        )

    def search_expenses(self, keyword):
        df = self.get_all_expenses()
        if df.empty:
            return df
        mask = (
            df["Category"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Description"].astype(str).str.contains(keyword, case=False, na=False)
            | df["ExpenseID"].astype(str).str.contains(keyword, case=False, na=False)
            | df["Date"].astype(str).str.contains(keyword, case=False, na=False)
        )
        return df[mask]

    def filter_by_category(self, category):
        df = self.get_all_expenses()
        if df.empty or category == "All":
            return df
        return df[df["Category"].astype(str) == str(category)]

    def filter_by_date_range(self, start_date, end_date):
        df = self.get_all_expenses()
        if df.empty:
            return df
        start = Helpers.parse_date(start_date)
        end = Helpers.parse_date(end_date)
        if not start or not end:
            return df
        result = []
        for _, row in df.iterrows():
            exp_date = Helpers.parse_date(row["Date"])
            if exp_date and start <= exp_date <= end:
                result.append(row)
        if result:
            return pd.DataFrame(result)
        return pd.DataFrame(columns=df.columns)

    def get_categories(self):
        return self.CATEGORIES

    def get_total_expenses(self):
        df = self.get_all_expenses()
        if df.empty:
            return 0.0
        try:
            return float(df["Amount"].sum())
        except Exception:
            return 0.0

    def get_expense_count(self):
        df = self.get_all_expenses()
        return len(df)