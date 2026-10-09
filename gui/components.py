"""
UIComponents - Reusable CustomTkinter UI components.
Provides factory methods for consistent UI elements across the app.
"""

import customtkinter as ctk


COLORS = {
    "primary": "#1F6AA5",
    "primary_hover": "#16568A",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "info": "#2980B9",
    "light_bg": "#F0F2F5",
    "card_bg": "#FFFFFF",
    "text_dark": "#2C3E50",
    "text_light": "#7F8C8D",
    "border": "#E0E0E0",
}

CARD_COLORS = [
    ("#3498DB", "#2980B9"),
    ("#E74C3C", "#C0392B"),
    ("#27AE60", "#229954"),
    ("#9B59B6", "#8E44AD"),
    ("#F39C12", "#E67E22"),
    ("#1ABC9C", "#16A085"),
    ("#34495E", "#2C3E50"),
]


def create_card(parent, title, value, icon="", color_idx=0):
    bg_color, accent_color = CARD_COLORS[color_idx % len(CARD_COLORS)]
    card = ctk.CTkFrame(parent, fg_color=card_fg(), corner_radius=12,
                        border_width=1, border_color=COLORS["border"])
    card.pack_propagate(False)

    accent = ctk.CTkFrame(card, fg_color=accent_color, corner_radius=10, height=6)
    accent.pack(fill="x", padx=10, pady=(10, 0))

    if icon:
        icon_label = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=28),
                                  text_color=accent_color)
        icon_label.pack(pady=(10, 0))

    title_label = ctk.CTkLabel(card, text=title,
                               font=ctk.CTkFont(size=13, weight="normal"),
                               text_color=COLORS["text_light"])
    title_label.pack(pady=(5, 0))

    value_label = ctk.CTkLabel(card, text=value,
                               font=ctk.CTkFont(size=22, weight="bold"),
                               text_color=COLORS["text_dark"])
    value_label.pack(pady=(2, 10))

    return card


def card_fg():
    if ctk.get_appearance_mode() == "Dark":
        return "#2B2B2B"
    return "#FFFFFF"


def create_section_header(parent, title, subtitle=""):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=20, pady=(15, 5))

    label = ctk.CTkLabel(frame, text=title,
                         font=ctk.CTkFont(size=24, weight="bold"),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white")
    label.pack(anchor="center")

    if subtitle:
        sub = ctk.CTkLabel(frame, text=subtitle,
                           font=ctk.CTkFont(size=13),
                           text_color=COLORS["text_light"])
        sub.pack(anchor="center", pady=(2, 0))

    return frame


def create_button(parent, text, command, fg_color=None, hover_color=None,
                  width=140, height=36, font_size=14):
    if fg_color is None:
        fg_color = COLORS["primary"]
    if hover_color is None:
        hover_color = COLORS["primary_hover"]
    btn = ctk.CTkButton(parent, text=text, command=command,
                        fg_color=fg_color, hover_color=hover_color,
                        width=width, height=height,
                        font=ctk.CTkFont(size=font_size, weight="bold"),
                        corner_radius=8)
    return btn


def create_input(parent, label_text, placeholder="", width=200):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=5, pady=3)

    label = ctk.CTkLabel(frame, text=label_text,
                         font=ctk.CTkFont(size=13),
                         text_color=COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white")
    label.pack(anchor="w")

    entry = ctk.CTkEntry(frame, placeholder_text=placeholder, width=width,
                         height=32, corner_radius=6,
                         font=ctk.CTkFont(size=13))
    entry.pack(fill="x", pady=(2, 0))
    return frame, entry


RIGHT_ALIGN_COLS = {
    "CostPrice", "SellingPrice", "Profit/Unit", "UnitPrice", "TotalAmount",
    "Amount", "TotalSales", "TotalExpenses", "TotalAmount", "TotalRevenue",
    "TotalProfit", "TotalCost", "TotalSpending", "TotalPurchases",
    "Quantity", "QuantitySold", "StockQuantity", "ReorderLevel",
    "PurchaseCount", "ProfitMargin", "Percentage",
}

CENTER_ALIGN_COLS = {
    "StockStatus", "Performance", "Category", "PaymentMethod", "SaleID",
    "ProductID", "CustomerID", "ExpenseID", "Date",
}


def _col_anchor(col_name):
    if col_name in RIGHT_ALIGN_COLS:
        return "e"
    if col_name in CENTER_ALIGN_COLS:
        return "center"
    return "w"


COL_WIDTHS = {
    "SaleID": 80, "ProductID": 90, "CustomerID": 90, "ExpenseID": 90,
    "Date": 100, "Product": 140, "Customer": 140, "ProductName": 140,
    "CustomerName": 140, "Category": 110, "Description": 180,
    "Quantity": 70, "QuantitySold": 80, "UnitPrice": 110, "TotalAmount": 120,
    "Amount": 110, "PaymentMethod": 120, "CostPrice": 110, "SellingPrice": 110,
    "Profit/Unit": 100, "StockQuantity": 90, "ReorderLevel": 90,
    "StockStatus": 110, "Performance": 120, "TotalSales": 120,
    "TotalExpenses": 120, "TotalRevenue": 120, "TotalProfit": 120,
    "TotalCost": 120, "TotalSpending": 120, "TotalPurchases": 120,
    "PurchaseCount": 90, "ProfitMargin": 100, "Percentage": 90,
    "City": 100, "Phone": 130, "Email": 180, "Month": 90,
}


def _col_width(col_name, col_count):
    return COL_WIDTHS.get(col_name, max(90, 800 // col_count))


def create_table(parent, columns, data, row_height=30, heading_height=35):
    frame = ctk.CTkFrame(parent, fg_color=card_fg(), corner_radius=10,
                         border_width=1, border_color=COLORS["border"])
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    if not data:
        empty = ctk.CTkLabel(frame, text="No data available",
                             font=ctk.CTkFont(size=14),
                             text_color=COLORS["text_light"])
        empty.pack(expand=True)
        return frame

    scroll = ctk.CTkScrollableFrame(frame, fg_color=card_fg())
    scroll.pack(fill="both", expand=True, padx=5, pady=5)

    n_cols = len(columns)
    for c in range(n_cols):
        scroll.grid_columnconfigure(c, weight=0, minsize=_col_width(columns[c], n_cols))

    header_frame = ctk.CTkFrame(scroll, fg_color=COLORS["primary"], corner_radius=6)
    header_frame.grid(row=0, column=0, columnspan=n_cols, sticky="ew", pady=(0, 2))

    for c, col_name in enumerate(columns):
        anchor = _col_anchor(col_name)
        lbl = ctk.CTkLabel(header_frame, text=col_name,
                           font=ctk.CTkFont(size=12, weight="bold"),
                           text_color="white", anchor=anchor)
        lbl.grid(row=0, column=c, sticky="ew", padx=2, pady=6)
        header_frame.grid_columnconfigure(c, weight=1)

    for row_idx, row_data in enumerate(data):
        row_color = card_fg() if row_idx % 2 == 0 else (
            "#F7F9FC" if ctk.get_appearance_mode() == "Light" else "#333333"
        )
        row_frame = ctk.CTkFrame(scroll, fg_color=row_color, corner_radius=4)
        row_frame.grid(row=row_idx + 1, column=0, columnspan=n_cols, sticky="ew", pady=1)

        for c, col_name in enumerate(columns):
            value = row_data.get(col_name, "")
            text_color = COLORS["text_dark"] if ctk.get_appearance_mode() == "Light" else "white"
            if col_name == "StockStatus":
                from utils.helpers import Helpers
                text_color = Helpers.stock_status_color(str(value))
            elif col_name == "Performance":
                from utils.helpers import Helpers
                text_color = Helpers.performance_color(str(value))
            elif col_name == "Category" and col_name in row_data:
                from utils.helpers import Helpers
                text_color = Helpers.customer_category_color(str(value))

            anchor = _col_anchor(col_name)
            lbl = ctk.CTkLabel(row_frame, text=str(value),
                               font=ctk.CTkFont(size=12),
                               text_color=text_color, anchor=anchor)
            lbl.grid(row=0, column=c, sticky="ew", padx=2, pady=4)
            row_frame.grid_columnconfigure(c, weight=1)

    return frame


def create_search_bar(parent, command, placeholder="Search..."):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=10, pady=(5, 0))

    entry = ctk.CTkEntry(frame, placeholder_text=placeholder, height=34,
                         corner_radius=8, font=ctk.CTkFont(size=13))
    entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
    entry.bind("<KeyRelease>", lambda e: command(entry.get()))

    btn = create_button(frame, "Search", lambda: command(entry.get()),
                        width=80, height=34)
    btn.pack(side="right")

    return frame, entry


def create_status_badge(parent, text, color):
    badge = ctk.CTkLabel(parent, text=text,
                         font=ctk.CTkFont(size=11, weight="bold"),
                         text_color="white", fg_color=color,
                         corner_radius=10, width=90, height=22)
    return badge