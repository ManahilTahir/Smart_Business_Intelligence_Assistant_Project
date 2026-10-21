"""
Smart Business BI - Main Application Entry Point
A Python-based desktop Business Intelligence application.
"""

import os
import sys
import json
import customtkinter as ctk

from utils.file_manager import FileManager
from managers.product_manager import ProductManager
from managers.customer_manager import CustomerManager
from managers.sales_manager import SalesManager
from managers.expense_manager import ExpenseManager
from managers.inventory_manager import InventoryManager
from analysis.data_analyzer import DataAnalyzer

from gui.dashboard import Dashboard
from gui.sales_page import SalesPage
from gui.products_page import ProductsPage
from gui.customers_page import CustomersPage
from gui.expenses_page import ExpensesPage
from gui.inventory_page import InventoryPage
from gui.analytics_page import AnalyticsPage
from gui.reports_page import ReportsPage
from gui.settings_page import SettingsPage

from gui.components import COLORS


class BusinessApp:
    """Main application class managing the GUI and business logic."""

    SETTINGS_FILE = "settings.json"
    NAV_ITEMS = [
        ("Dashboard", "🏠"),
        ("Sales", "💰"),
        ("Products", "📦"),
        ("Customers", "👥"),
        ("Expenses", "📉"),
        ("Inventory", "📋"),
        ("Analytics", "📊"),
        ("Reports", "📄"),
        ("Settings", "⚙️"),
    ]

    def __init__(self):
        self._setup_data_directory()
        self._init_managers()
        self._init_analyzer()
        self._load_settings()
        self._init_gui()
        self._init_pages()
        self.current_page = None
        self.show_page("Dashboard")

    def _setup_data_directory(self):
        if getattr(sys, "frozen", False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, "data")
        os.makedirs(self.data_dir, exist_ok=True)
        os.chdir(base_dir)

    def _init_managers(self):
        self.file_manager = FileManager()
        self.product_manager = ProductManager(self.file_manager)
        self.customer_manager = CustomerManager(self.file_manager)
        self.sales_manager = SalesManager(self.file_manager)
        self.expense_manager = ExpenseManager(self.file_manager)
        self.inventory_manager = InventoryManager(self.product_manager)

    def _init_analyzer(self):
        self.analyzer = DataAnalyzer(
            sales_manager=self.sales_manager,
            product_manager=self.product_manager,
            customer_manager=self.customer_manager,
            expense_manager=self.expense_manager,
            inventory_manager=self.inventory_manager,
        )

    def _load_settings(self):
        self.business_name = "BusinessHub"
        self.currency = "PKR"
        self.theme = "System"

        settings_path = os.path.join(self.base_dir, self.SETTINGS_FILE)
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r") as f:
                    settings = json.load(f)
                    self.business_name = settings.get("business_name", self.business_name)
                    self.currency = settings.get("currency", self.currency)
                    self.theme = settings.get("theme", self.theme)
            except Exception:
                pass

    def save_settings(self):
        settings = {
            "business_name": self.business_name,
            "currency": self.currency,
            "theme": self.theme,
        }
        settings_path = os.path.join(self.base_dir, self.SETTINGS_FILE)
        try:
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get_business_name(self):
        return self.business_name

    def set_business_name(self, name):
        self.business_name = name

    def get_currency(self):
        return self.currency

    def set_currency(self, currency):
        self.currency = currency

    def get_theme(self):
        return self.theme

    def set_theme(self, theme):
        self.theme = theme

    def _init_gui(self):
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("BusinessHub - Business Intelligence & Analytics")
        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_main_content()
        self._build_footer()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self.root, width=220, corner_radius=0,
                                     fg_color=COLORS["primary"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", pady=(15, 5))

        logo_circle = ctk.CTkFrame(logo_frame, fg_color="#16568A", corner_radius=50,
                                    width=80, height=80)
        logo_circle.pack(pady=(5, 5))
        logo_circle.pack_propagate(False)
        ctk.CTkLabel(logo_circle, text="📊", font=ctk.CTkFont(size=40)).pack(expand=True)

        ctk.CTkLabel(logo_frame, text="BusinessHub",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white").pack(pady=(2, 0))
        ctk.CTkLabel(logo_frame, text="Business Intelligence & Analytics",
                     font=ctk.CTkFont(size=11),
                     text_color="#B0D4F1").pack(pady=(1, 0))

        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(fill="both", expand=True, pady=10)

        self.nav_buttons = {}
        for item_name, icon in self.NAV_ITEMS:
            btn = ctk.CTkButton(
                nav_frame, text=f"  {icon}  {item_name}",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent", hover_color="#16568A",
                text_color="white", anchor="w", height=42,
                corner_radius=8,
                command=lambda name=item_name: self.show_page(name),
            )
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[item_name] = btn

        status_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        status_frame.pack(fill="x", side="bottom", pady=10)
        ctk.CTkLabel(status_frame, text="v1.0 | No AI/ML",
                     font=ctk.CTkFont(size=10),
                     text_color="#B0D4F1").pack()

    def _build_main_content(self):
        self.content_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def _build_footer(self):
        footer = ctk.CTkFrame(self.root, height=28, fg_color=COLORS["primary"],
                              corner_radius=0)
        footer.grid(row=1, column=0, columnspan=2, sticky="ew")
        ctk.CTkLabel(footer, text="Developed by: Manahil Tahir",
                     font=ctk.CTkFont(size=11),
                     text_color="white").pack(side="right", padx=15, pady=4)

    def _init_pages(self):
        self.pages = {
            "Dashboard": Dashboard(self.content_frame, self),
            "Sales": SalesPage(self.content_frame, self),
            "Products": ProductsPage(self.content_frame, self),
            "Customers": CustomersPage(self.content_frame, self),
            "Expenses": ExpensesPage(self.content_frame, self),
            "Inventory": InventoryPage(self.content_frame, self),
            "Analytics": AnalyticsPage(self.content_frame, self),
            "Reports": ReportsPage(self.content_frame, self),
            "Settings": SettingsPage(self.content_frame, self),
        }

    def show_page(self, page_name):
        if self.current_page and self.current_page in self.pages:
            self.pages[self.current_page].hide()

        if page_name in self.pages:
            self.pages[page_name].show()
            self.current_page = page_name
            self._update_nav_buttons(page_name)

    def _update_nav_buttons(self, active_name):
        for name, btn in self.nav_buttons.items():
            if name == active_name:
                btn.configure(fg_color="#16568A", hover_color="#0E4470")
            else:
                btn.configure(fg_color="transparent", hover_color="#16568A")

    def run(self):
        self.root.mainloop()


def main():
    app = BusinessApp()
    app.run()


if __name__ == "__main__":
    main()