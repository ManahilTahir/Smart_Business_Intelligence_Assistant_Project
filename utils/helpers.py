"""
Helpers - Utility helper functions used across the application.
"""

from datetime import datetime, timedelta
import random


class Helpers:
    """Common helper functions for formatting and dates."""

    CURRENCY_SYMBOLS = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "PKR": "₨",
        "INR": "₹",
        "AED": "د.إ",
        "SAR": "﷼",
        "CAD": "C$",
        "AUD": "A$",
        "JPY": "¥",
        "CNY": "¥",
        "CHF": "CHF",
        "TRY": "₺",
    }

    SYMBOL_BEFORE_NUMBER = {"$", "€", "£", "₨", "₹", "¥", "₺", "C$", "A$", "CHF"}

    @staticmethod
    def format_currency(amount, currency="PKR"):
        try:
            value = float(amount)
        except (ValueError, TypeError):
            value = 0.0
        symbol = Helpers.CURRENCY_SYMBOLS.get(currency, currency)
        if symbol in Helpers.SYMBOL_BEFORE_NUMBER:
            return f"{symbol}{value:,.2f}"
        return f"{value:,.2f} {symbol}"

    @staticmethod
    def format_percentage(value, decimals=1):
        try:
            val = float(value)
        except (ValueError, TypeError):
            val = 0.0
        return f"{val:.{decimals}f}%"

    @staticmethod
    def format_number(value):
        try:
            val = float(value)
        except (ValueError, TypeError):
            val = 0.0
        if val == int(val):
            return f"{int(val):,}"
        return f"{val:,.2f}"

    @staticmethod
    def today_string():
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def current_month_string():
        return datetime.now().strftime("%Y-%m")

    @staticmethod
    def parse_date(date_string, date_format="%Y-%m-%d"):
        try:
            return datetime.strptime(str(date_string).strip(), date_format)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def get_month_from_date(date_string):
        dt = Helpers.parse_date(date_string)
        if dt:
            return dt.strftime("%Y-%m")
        return ""

    @staticmethod
    def get_month_label(date_string):
        dt = Helpers.parse_date(date_string)
        if dt:
            return dt.strftime("%b %Y")
        return str(date_string)

    @staticmethod
    def previous_month_string():
        prev = datetime.now() - timedelta(days=30)
        return prev.strftime("%Y-%m")

    @staticmethod
    def safe_divide(numerator, denominator):
        try:
            denom = float(denominator)
            if denom == 0:
                return 0.0
            return float(numerator) / denom
        except (ValueError, TypeError, ZeroDivisionError):
            return 0.0

    @staticmethod
    def classify_stock_status(current_stock, reorder_level):
        try:
            stock = int(current_stock)
            reorder = int(reorder_level)
        except (ValueError, TypeError):
            return "UNKNOWN"
        if stock == 0:
            return "OUT OF STOCK"
        if stock <= reorder:
            return "LOW STOCK"
        return "IN STOCK"

    @staticmethod
    def stock_status_color(status):
        colors = {
            "IN STOCK": "#2ECC71",
            "LOW STOCK": "#F39C12",
            "OUT OF STOCK": "#E74C3C",
            "UNKNOWN": "#95A5A6",
        }
        return colors.get(status, "#95A5A6")

    @staticmethod
    def classify_product_performance(total_revenue, total_profit, avg_revenue, avg_profit):
        if total_revenue >= avg_revenue * 1.5 and total_profit >= avg_profit * 1.2:
            return "High Performer"
        if total_revenue >= avg_revenue * 0.5 and total_profit >= 0:
            return "Good Performer"
        return "Low Performer"

    @staticmethod
    def performance_color(category):
        colors = {
            "High Performer": "#27AE60",
            "Good Performer": "#2980B9",
            "Low Performer": "#E67E22",
        }
        return colors.get(category, "#95A5A6")

    @staticmethod
    def classify_customer_category(total_spending, vip_threshold, regular_threshold):
        if total_spending >= vip_threshold:
            return "VIP"
        if total_spending >= regular_threshold:
            return "Regular"
        return "Occasional"

    @staticmethod
    def customer_category_color(category):
        colors = {
            "VIP": "#9B59B6",
            "Regular": "#2980B9",
            "Occasional": "#7F8C8D",
        }
        return colors.get(category, "#95A5A6")

    @staticmethod
    def random_date_in_range(start_date, end_date):
        start = Helpers.parse_date(start_date)
        end = Helpers.parse_date(end_date)
        if not start or not end:
            return Helpers.today_string()
        delta = end - start
        random_days = random.randint(0, delta.days)
        result = start + timedelta(days=random_days)
        return result.strftime("%Y-%m-%d")