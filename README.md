# Smart Business BI

Smart Business BI is a Python-based desktop Business Intelligence application designed to help small businesses analyze sales, expenses, products, customers, and inventory through an easy-to-use CustomTkinter interface. It uses Object-Oriented Programming, Pandas, NumPy, and traditional data-analysis techniques to transform raw business data into meaningful business insights.

## Project Overview

This application provides a complete desktop-based business intelligence solution for small business owners. It allows users to manage and analyze sales, products, customers, expenses, and inventory data through a professional graphical interface. The application calculates key business metrics such as total sales, net profit, profit margins, best-selling products, customer spending patterns, and generates rule-based business insights.

## Problem Statement

Small business owners often struggle to understand their business data because they lack affordable, easy-to-use analytics tools. Most existing BI solutions are cloud-based, expensive, or too complex. This project provides a free, offline, desktop-based solution that transforms raw CSV data into actionable business insights without requiring any AI or machine learning.

## Objectives

- Provide a professional desktop GUI for business data management
- Demonstrate Object-Oriented Programming principles in Python
- Use Pandas for practical data analysis operations
- Use NumPy for numerical and statistical calculations
- Generate rule-based business insights from actual data
- Handle CSV file storage with automatic file creation
- Validate all user inputs with clear error messages
- Keep the code modular, beginner-friendly, and well-organized

## Features

### Dashboard
- KPI cards: Total Sales, Total Expenses, Net Profit, Profit Margin, Total Products, Total Customers, Low Stock Items
- Data-Based Business Insights generated from actual data

### Sales Management
- Add, view, search, filter, update, and delete sales records
- Automatic Total Amount calculation (Quantity x Unit Price)
- Payment method tracking

### Product Management
- Add, edit, delete, search, and filter products by category
- Automatic profit-per-unit calculation
- Stock quantity and reorder level tracking

### Customer Management
- Add, edit, delete, and search customers
- Automatic total purchases tracking
- Customer categorization (VIP, Regular, Occasional)

### Expense Management
- Add, edit, delete, search, and filter expenses
- Category-based filtering (Rent, Salary, Utilities, Marketing, etc.)
- Date-based filtering

### Inventory Management
- Automatic stock status classification (In Stock, Low Stock, Out of Stock)
- Visual status indicators
- Restock functionality
- Inventory value calculation

### Analytics
- Sales analysis: total, average, max, min, quantity sold, by product/category/month
- Expense analysis: total, average, highest, by category, monthly trends
- Product performance classification (High/Good/Low Performer)
- Customer analysis with spending and purchase counts

### Reports
- Sales Report, Expense Report, Profit Report, Inventory Report
- All reports generated from current data

### Settings
- Configurable business name
- Currency selection (PKR, USD, AED)
- Theme appearance (Light, Dark, System)
- Configurable customer category thresholds

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming Language |
| Tkinter / CustomTkinter | GUI Framework |
| Pandas | Data Analysis and CSV Handling |
| NumPy | Numerical Calculations |
| CSV Files | Data Storage |

## OOP Concepts Used

- **Classes**: BusinessApp, Dashboard, SalesManager, ProductManager, CustomerManager, ExpenseManager, InventoryManager, DataAnalyzer, FileManager, Validators, Helpers, Calculations
- **Objects**: All managers and pages are instantiated as objects
- **Encapsulation**: Each manager class encapsulates its data operations
- **Instance Attributes & Methods**: Used throughout all classes
- **Separation of Concerns**: GUI classes handle interface, managers handle business logic, analysis classes handle calculations

## Pandas Functionality Used

- `DataFrame` creation and manipulation
- `read_csv()` and `to_csv()` for file I/O
- `groupby()` for aggregations
- `sum()`, `mean()`, `max()`, `min()` for calculations
- `sort_values()` for sorting
- `merge()` for joining dataframes
- Boolean filtering and indexing
- `str.contains()` for search operations
- Date operations for monthly grouping

## NumPy Functionality Used

- `np.mean()` - Average calculations
- `np.median()` - Median calculations
- `np.std()` - Standard deviation
- `np.sum()` - Summations
- `np.max()` / `np.min()` - Maximum/Minimum values
- `np.array()` - Array conversions
- NaN handling for robust calculations

## Project Structure

```
SmartBusinessBI/
│
├── main.py                    # Application entry point
├── generate_data.py           # Sample data generator
│
├── gui/
│   ├── components.py          # Reusable UI components
│   ├── dashboard.py           # Dashboard page
│   ├── sales_page.py          # Sales management page
│   ├── products_page.py       # Product management page
│   ├── customers_page.py      # Customer management page
│   ├── expenses_page.py       # Expense management page
│   ├── inventory_page.py      # Inventory management page
│   ├── analytics_page.py      # Analytics page
│   ├── reports_page.py        # Reports page
│   └── settings_page.py       # Settings page
│
├── managers/
│   ├── sales_manager.py       # Sales CRUD operations
│   ├── product_manager.py     # Product CRUD operations
│   ├── customer_manager.py    # Customer CRUD operations
│   ├── expense_manager.py     # Expense CRUD operations
│   └── inventory_manager.py   # Inventory status management
│
├── analysis/
│   ├── data_analyzer.py       # Main analysis engine
│   └── calculations.py        # NumPy-based calculations
│
├── data/
│   ├── sales.csv              # Sales data
│   ├── products.csv           # Product data
│   ├── customers.csv          # Customer data
│   ├── expenses.csv           # Expense data
│   └── inventory.csv          # Inventory data (derived)
│
├── utils/
│   ├── file_manager.py        # CSV file operations
│   ├── validators.py          # Input validation
│   └── helpers.py             # Helper functions
│
├── assets/
│   └── logo.png               # Application logo
│
└── README.md                  # This file
```

## How to Install

1. Ensure Python 3.10 or higher is installed
2. Install required packages:

```bash
pip install customtkinter pandas numpy
```

## How to Run

Navigate to the SmartBusinessBI directory and run:

```bash
python main.py
```

To regenerate sample data:

```bash
python generate_data.py
```

## Sample Data

The application comes with realistic sample data:
- **Products**: 20 items across Electronics, Furniture, Stationery, and Appliances categories
- **Customers**: 30 fictional customers from various Pakistani cities
- **Sales**: 120+ sales records spanning the year 2025
- **Expenses**: 55+ expense records across 8 categories

All data is fictional and does not contain real personal information.

## Data-Based Insights Examples

The application generates insights such as:
- "Webcam is currently the best-selling product with 68 units sold."
- "Technology is the highest expense category."
- "Profit margin is currently 16.1%."
- "Asad Malik has the highest total purchase value."
- "Sales decreased by 75.4% compared with the previous month."

These insights are generated using rule-based Python logic, not AI or machine learning.

## Important Notes

- **No AI/ML**: This version uses only traditional programming and data analysis
- **Offline**: The application runs entirely offline
- **CSV Storage**: All data is stored in CSV files, no database required
- **Currency Display**: Changing currency only changes display, not stored values

## Future Improvements

### Version 2
- Machine Learning for sales forecasting
- Customer segmentation using clustering algorithms
- Anomaly detection for unusual transactions
- Advanced data visualization with charts

### Version 3
- AI business assistant for natural-language questions
- AI-generated business recommendations
- Predictive analytics for inventory management
- Automated report generation and scheduling