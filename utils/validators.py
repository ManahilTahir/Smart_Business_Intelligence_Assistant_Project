"""
Validators - Input validation for all application forms.
Provides static methods to validate user inputs.
"""

import re
from datetime import datetime


class Validators:
    """Static validation methods for user inputs."""

    @staticmethod
    def is_not_empty(value):
        if value is None:
            return False
        return str(value).strip() != ""

    @staticmethod
    def is_valid_number(value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_non_negative_number(value):
        if not Validators.is_valid_number(value):
            return False
        return float(value) >= 0

    @staticmethod
    def is_positive_number(value):
        if not Validators.is_valid_number(value):
            return False
        return float(value) > 0

    @staticmethod
    def is_valid_integer(value):
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_non_negative_integer(value):
        if not Validators.is_valid_integer(value):
            return False
        return int(value) >= 0

    @staticmethod
    def is_valid_email(email):
        if not email or not str(email).strip():
            return True
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, str(email).strip()) is not None

    @staticmethod
    def is_valid_phone(phone):
        if not phone or not str(phone).strip():
            return True
        cleaned = re.sub(r'[\s\-\(\)\+]', '', str(phone))
        return cleaned.isdigit() and len(cleaned) >= 7

    @staticmethod
    def is_valid_date(date_string, date_format="%Y-%m-%d"):
        if not date_string or not str(date_string).strip():
            return False
        try:
            datetime.strptime(str(date_string).strip(), date_format)
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_product(name, category, cost_price, selling_price, stock, reorder):
        errors = []
        if not Validators.is_not_empty(name):
            errors.append("Product name cannot be empty.")
        if not Validators.is_not_empty(category):
            errors.append("Category cannot be empty.")
        if not Validators.is_non_negative_number(cost_price):
            errors.append("Cost price must be a non-negative number.")
        if not Validators.is_non_negative_number(selling_price):
            errors.append("Selling price must be a non-negative number.")
        if not Validators.is_non_negative_integer(stock):
            errors.append("Stock quantity must be a non-negative integer.")
        if not Validators.is_non_negative_integer(reorder):
            errors.append("Reorder level must be a non-negative integer.")
        return errors

    @staticmethod
    def validate_customer(name, phone, email):
        errors = []
        if not Validators.is_not_empty(name):
            errors.append("Customer name cannot be empty.")
        if not Validators.is_valid_phone(phone):
            errors.append("Phone number is not valid.")
        if not Validators.is_valid_email(email):
            errors.append("Email address is not valid.")
        return errors

    @staticmethod
    def validate_sale(date, product, customer, quantity, unit_price, payment_method):
        errors = []
        if not Validators.is_valid_date(date):
            errors.append("Date is not valid (use YYYY-MM-DD format).")
        if not Validators.is_not_empty(product):
            errors.append("Product must be selected.")
        if not Validators.is_not_empty(customer):
            errors.append("Customer must be selected.")
        if not Validators.is_positive_integer(quantity):
            errors.append("Quantity must be a positive integer.")
        if not Validators.is_positive_number(unit_price):
            errors.append("Unit price must be a positive number.")
        if not Validators.is_not_empty(payment_method):
            errors.append("Payment method must be selected.")
        return errors

    @staticmethod
    def validate_expense(date, category, description, amount):
        errors = []
        if not Validators.is_valid_date(date):
            errors.append("Date is not valid (use YYYY-MM-DD format).")
        if not Validators.is_not_empty(category):
            errors.append("Category cannot be empty.")
        if not Validators.is_not_empty(description):
            errors.append("Description cannot be empty.")
        if not Validators.is_positive_number(amount):
            errors.append("Amount must be a positive number.")
        return errors

    @staticmethod
    def is_positive_integer(value):
        if not Validators.is_valid_integer(value):
            return False
        return int(value) > 0