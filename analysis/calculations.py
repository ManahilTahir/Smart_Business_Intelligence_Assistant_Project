"""
Calculations - Core business calculation functions using NumPy.
Provides static methods for numerical business calculations.
"""

import numpy as np
from utils.helpers import Helpers


class Calculations:
    """Static business calculation methods using NumPy."""

    @staticmethod
    def mean(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.mean(arr))

    @staticmethod
    def median(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.median(arr))

    @staticmethod
    def std_dev(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.std(arr))

    @staticmethod
    def total(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.sum(arr))

    @staticmethod
    def maximum(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.max(arr))

    @staticmethod
    def minimum(values):
        arr = Calculations._to_array(values)
        if arr.size == 0:
            return 0.0
        return float(np.min(arr))

    @staticmethod
    def percentage(part, whole):
        return Helpers.safe_divide(part, whole) * 100

    @staticmethod
    def profit_margin(net_profit, revenue):
        return Helpers.safe_divide(net_profit, revenue) * 100

    @staticmethod
    def net_profit(revenue, cost_of_goods, expenses):
        return float(revenue) - float(cost_of_goods) - float(expenses)

    @staticmethod
    def percent_change(old_value, new_value):
        if old_value == 0:
            return 0.0
        return ((float(new_value) - float(old_value)) / float(old_value)) * 100

    @staticmethod
    def _to_array(values):
        try:
            arr = np.array(values, dtype=float)
            arr = arr[~np.isnan(arr)]
            return arr
        except Exception:
            return np.array([])