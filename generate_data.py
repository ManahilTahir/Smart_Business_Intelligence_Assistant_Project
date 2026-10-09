"""
generate_data - Creates realistic sample CSV data for the application.
Run this script to populate all CSV files with sample business data.
"""

import os
import random
from datetime import datetime, timedelta
from utils.file_manager import FileManager
from managers.product_manager import ProductManager
from managers.customer_manager import CustomerManager
from managers.sales_manager import SalesManager
from managers.expense_manager import ExpenseManager


def generate_sample_data():
    fm = FileManager()
    pm = ProductManager(fm)
    cm = CustomerManager(fm)
    sm = SalesManager(fm)
    em = ExpenseManager(fm)

    products_data = [
        ("Laptop", "Electronics", 45000, 65000, 45, 10),
        ("Desktop PC", "Electronics", 55000, 80000, 25, 8),
        ("Wireless Mouse", "Electronics", 800, 1500, 100, 20),
        ("USB Keyboard", "Electronics", 1200, 2500, 80, 15),
        ("Monitor 24 inch", "Electronics", 12000, 18000, 35, 10),
        ("Printer", "Electronics", 15000, 22000, 15, 5),
        ("Webcam", "Electronics", 2500, 4500, 40, 10),
        ("Headphones", "Electronics", 2000, 4000, 60, 15),
        ("Smartphone", "Electronics", 35000, 55000, 50, 15),
        ("Tablet", "Electronics", 25000, 40000, 30, 10),
        ("Office Chair", "Furniture", 8000, 15000, 20, 5),
        ("Desk", "Furniture", 12000, 20000, 15, 5),
        ("Bookshelf", "Furniture", 10000, 18000, 10, 3),
        ("Filing Cabinet", "Furniture", 9000, 16000, 8, 3),
        ("A4 Paper Pack", "Stationery", 500, 900, 200, 50),
        ("Ballpoint Pens Box", "Stationery", 300, 600, 150, 40),
        ("Stapler", "Stationery", 400, 800, 50, 15),
        ("Notebook", "Stationery", 200, 450, 120, 30),
        ("Coffee Maker", "Appliances", 7000, 12000, 18, 5),
        ("Water Dispenser", "Appliances", 9000, 15000, 0, 5),
    ]

    for name, cat, cost, sell, stock, reorder in products_data:
        pm.add_product(name, cat, cost, sell, stock, reorder)

    cities = ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Peshawar",
              "Multan", "Faisalabad", "Quetta", "Hyderabad", "Sialkot"]
    first_names = ["Ahmed", "Bilal", "Sana", "Fatima", "Usman", "Ayesha",
                   "Kamran", "Nida", "Sajid", "Hina", "Tariq", "Maria",
                   "Imran", "Zain", "Aisha", "Bilal", "Sadia", "Faisal",
                   "Nadia", "Asad", "Hira", "Owais", "Mahnoor", "Ali",
                   "Rabia", "Shahid", "Amna", "Gohar", "Kiran", "Junaid"]
    last_names = ["Khan", "Ahmed", "Malik", "Sheikh", "Butt", "Chaudhry",
                  "Raza", "Hashmi", "Qureshi", "Siddiqui"]

    for i in range(30):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"03{random.randint(10, 49)}-{random.randint(1000000, 9999999)}"
        email = f"{name.lower().replace(' ', '.')}@email.com"
        city = random.choice(cities)
        cm.add_customer(name, phone, email, city)

    product_names = pm.get_product_names()
    customer_names = cm.get_customer_names()
    payment_methods = sm.get_payment_methods()
    start_date = "2025-01-01"
    end_date = "2025-12-31"

    for _ in range(120):
        prod_name = random.choice(product_names)
        cust_name = random.choice(customer_names)
        qty = random.randint(1, 10)
        unit_price = pm.get_selling_price_by_name(prod_name)
        date = _random_date(start_date, end_date)
        method = random.choice(payment_methods)
        sm.add_sale(date, prod_name, cust_name, qty, unit_price, method)
        pm.reduce_stock(prod_name, qty)
        cust_id = cm.get_customer_id_by_name(cust_name)
        total = qty * unit_price
        cm.update_total_purchases(cust_id, total)

    expense_categories = em.get_categories()
    expense_descriptions = {
        "Rent": ["Monthly office rent", "Warehouse rent payment"],
        "Salary": ["Staff salaries", "Manager salary", "Employee wages"],
        "Utilities": ["Electricity bill", "Water bill", "Gas bill", "Internet bill"],
        "Marketing": ["Facebook ads", "Google ads", "Print marketing", "Promotional event"],
        "Transportation": ["Delivery fuel", "Vehicle maintenance", "Courier charges"],
        "Inventory": ["Stock purchase", "Raw materials", "Supplier payment"],
        "Technology": ["Software license", "Server hosting", "IT equipment"],
        "Other": ["Miscellaneous expense", "Office supplies", "Bank charges"],
    }

    for _ in range(55):
        cat = random.choice(expense_categories)
        desc = random.choice(expense_descriptions.get(cat, ["General expense"]))
        amount = round(random.uniform(5000, 80000), 2)
        date = _random_date(start_date, end_date)
        em.add_expense(date, cat, desc, amount)

    print("Sample data generated successfully!")
    print(f"  Products: {pm.get_total_products()}")
    print(f"  Customers: {cm.get_total_customers()}")
    print(f"  Sales: {sm.get_sales_count()}")
    print(f"  Expenses: {em.get_expense_count()}")


def _random_date(start_str, end_str):
    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime("%Y-%m-%d")


if __name__ == "__main__":
    generate_sample_data()