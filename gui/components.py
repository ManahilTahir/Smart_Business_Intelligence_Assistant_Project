"""
UIComponents - Reusable CustomTkinter UI components.
Provides factory methods for consistent UI elements across the app.
"""

import customtkinter as ctk
from tkinter import Canvas, BOTH, LEFT, RIGHT, Y, X


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
    card = ctk.CTkFrame(parent, fg_color=accent_color, corner_radius=12)
    card.pack_propagate(False)

    if icon:
        icon_label = ctk.CTkLabel(card, text=icon, font=ctk.CTkFont(size=28),
                                  text_color="white")
        icon_label.pack(pady=(12, 0))

    title_label = ctk.CTkLabel(card, text=title,
                               font=ctk.CTkFont(size=13, weight="bold"),
                               text_color="#E8E8E8")
    title_label.pack(pady=(5, 0))

    value_label = ctk.CTkLabel(card, text=value,
                               font=ctk.CTkFont(size=22, weight="bold"),
                               text_color="white")
    value_label.pack(pady=(2, 12))

    return card


def card_fg():
    if ctk.get_appearance_mode() == "Dark":
        return "#2B2B2B"
    return "#FFFFFF"


def text_fg():
    if ctk.get_appearance_mode() == "Dark":
        return "#E8E8E8"
    return COLORS["text_dark"]


def subtext_fg():
    if ctk.get_appearance_mode() == "Dark":
        return "#AAAAAA"
    return COLORS["text_light"]


def canvas_bg():
    if ctk.get_appearance_mode() == "Dark":
        return "#2B2B2B"
    return "#FFFFFF"


def grid_line_color():
    if ctk.get_appearance_mode() == "Dark":
        return "#444444"
    return "#E0E0E0"


def create_section_header(parent, title, subtitle=""):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(fill="x", padx=20, pady=(15, 5))

    label = ctk.CTkLabel(frame, text=title,
                         font=ctk.CTkFont(size=24, weight="bold"),
                         text_color=text_fg())
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

    n_cols = len(columns)
    col_widths = [_col_width(c, n_cols) for c in columns]

    header_frame = ctk.CTkFrame(frame, fg_color=COLORS["primary"], corner_radius=6)
    header_frame.pack(fill="x", padx=5, pady=(5, 0))

    for c, col_name in enumerate(columns):
        lbl = ctk.CTkLabel(header_frame, text=col_name,
                           font=ctk.CTkFont(size=12, weight="bold"),
                           text_color="white", anchor="center")
        lbl.grid(row=0, column=c, sticky="ew", padx=2, pady=6, ipadx=4)
        header_frame.grid_columnconfigure(c, weight=1, minsize=col_widths[c])

    scroll = ctk.CTkScrollableFrame(frame, fg_color=card_fg())
    scroll.pack(fill="both", expand=True, padx=5, pady=(0, 5))

    for c in range(n_cols):
        scroll.grid_columnconfigure(c, weight=1, minsize=col_widths[c])

    for row_idx, row_data in enumerate(data):
        row_color = card_fg() if row_idx % 2 == 0 else (
            "#F7F9FC" if ctk.get_appearance_mode() == "Light" else "#333333"
        )

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

            anchor = "center"
            lbl = ctk.CTkLabel(scroll, text=str(value),
                               font=ctk.CTkFont(size=12),
                               text_color=text_color, anchor=anchor,
                               fg_color=row_color, corner_radius=4)
            lbl.grid(row=row_idx, column=c, sticky="ew", padx=2, pady=1, ipadx=4, ipady=3)

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

CHART_COLORS = ["#3498DB", "#E74C3C", "#27AE60", "#9B59B6", "#F39C12",
                "#1ABC9C", "#34495E", "#E67E22", "#2ECC71", "#D35400",
                "#8E44AD", "#16A085", "#2980B9", "#C0392B"]


def create_bar_chart(parent, title, labels, values, color="#3498DB", height=220):
    frame = ctk.CTkFrame(parent, fg_color=card_fg(), corner_radius=10,
                         border_width=1, border_color=COLORS["border"])
    frame.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(8, 2))

    if not labels or not values:
        ctk.CTkLabel(frame, text="No data", font=ctk.CTkFont(size=12),
                     text_color=COLORS["text_light"]).pack(pady=20)
        return frame

    chart_wrap = ctk.CTkFrame(frame, fg_color=card_fg())
    chart_wrap.pack(fill="both", expand=True, padx=5, pady=(0, 8))

    canvas = Canvas(chart_wrap, bg=card_fg(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_chart(event=None):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 50 or h < 50:
            return
        n = len(labels)
        max_val = max(values) if max(values) > 0 else 1
        left_pad = 50
        bottom_pad = 45
        top_pad = 15
        right_pad = 15
        chart_w = w - left_pad - right_pad
        chart_h = h - bottom_pad - top_pad
        bar_w = chart_w / n * 0.65
        gap = chart_w / n * 0.35

        for i in range(5):
            y = top_pad + chart_h - (chart_h * i / 4)
            val = max_val * i / 4
            canvas.create_line(left_pad, y, w - right_pad, y, fill="#E0E0E0", dash=(2, 2))
            canvas.create_text(left_pad - 5, y, text=f"{val:,.0f}", anchor="e",
                               font=("Arial", 8), fill="#7F8C8D")

        for i, (label, val) in enumerate(zip(labels, values)):
            x = left_pad + i * (bar_w + gap) + gap / 2
            bar_h = (val / max_val) * chart_h if max_val > 0 else 0
            y_top = top_pad + chart_h - bar_h
            bar_color = CHART_COLORS[i % len(CHART_COLORS)] if color == "multi" else color
            canvas.create_rectangle(x, y_top, x + bar_w, top_pad + chart_h,
                                    fill=bar_color, outline="")
            canvas.create_text(x + bar_w / 2, top_pad + chart_h + 8, text=str(label)[:10],
                               anchor="n", font=("Arial", 8), fill="#2C3E50", angle=0)
            if bar_h > 20:
                canvas.create_text(x + bar_w / 2, y_top - 5, text=f"{val:,.0f}",
                                   anchor="s", font=("Arial", 8), fill="#2C3E50")

    canvas.bind("<Configure>", draw_chart)
    chart_wrap.after(100, lambda: draw_chart())
    return frame


def create_pie_chart(parent, title, labels, values, height=220):
    import math
    frame = ctk.CTkFrame(parent, fg_color=card_fg(), corner_radius=10,
                         border_width=1, border_color=COLORS["border"])
    frame.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(8, 2))

    if not labels or not values:
        ctk.CTkLabel(frame, text="No data", font=ctk.CTkFont(size=12),
                     text_color=COLORS["text_light"]).pack(pady=20)
        return frame

    chart_wrap = ctk.CTkFrame(frame, fg_color=card_fg())
    chart_wrap.pack(fill="both", expand=True, padx=5, pady=(0, 8))

    canvas = Canvas(chart_wrap, bg=card_fg(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_chart(event=None):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 50 or h < 50:
            return
        total = sum(values)
        if total <= 0:
            return
        cx = w * 0.35
        cy = h / 2
        radius = min(w * 0.3, h * 0.4)
        start_angle = 90

        for i, (label, val) in enumerate(zip(labels, values)):
            extent = (val / total) * 360
            color = CHART_COLORS[i % len(CHART_COLORS)]
            canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius,
                              start=start_angle, extent=-extent, fill=color, outline="white", style="pieslice")
            mid_angle = math.radians(start_angle - extent / 2)
            lx = cx + (radius * 0.6) * math.cos(mid_angle)
            ly = cy - (radius * 0.6) * math.sin(mid_angle)
            pct = (val / total) * 100
            if pct > 5:
                canvas.create_text(lx, ly, text=f"{pct:.0f}%", font=("Arial", 9, "bold"), fill="white")
            start_angle -= extent

        legend_x = w * 0.7
        for i, (label, val) in enumerate(zip(labels, values)):
            color = CHART_COLORS[i % len(CHART_COLORS)]
            ly = 20 + i * 20
            if ly > h - 10:
                break
            canvas.create_rectangle(legend_x, ly, legend_x + 12, ly + 12, fill=color, outline="")
            canvas.create_text(legend_x + 16, ly + 6, text=str(label)[:12], anchor="w",
                               font=("Arial", 9), fill="#2C3E50")

    canvas.bind("<Configure>", draw_chart)
    chart_wrap.after(100, lambda: draw_chart())
    return frame


def create_line_chart(parent, title, labels, values, color="#2980B9", height=220):
    frame = ctk.CTkFrame(parent, fg_color=card_fg(), corner_radius=10,
                         border_width=1, border_color=COLORS["border"])
    frame.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkLabel(frame, text=title, font=ctk.CTkFont(size=14, weight="bold"),
                 text_color=COLORS["primary"]).pack(anchor="w", padx=10, pady=(8, 2))

    if not labels or not values:
        ctk.CTkLabel(frame, text="No data", font=ctk.CTkFont(size=12),
                     text_color=COLORS["text_light"]).pack(pady=20)
        return frame

    chart_wrap = ctk.CTkFrame(frame, fg_color=card_fg())
    chart_wrap.pack(fill="both", expand=True, padx=5, pady=(0, 8))

    canvas = Canvas(chart_wrap, bg=card_fg(), highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    def draw_chart(event=None):
        canvas.delete("all")
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 50 or h < 50:
            return
        n = len(labels)
        max_val = max(values) if max(values) > 0 else 1
        min_val = min(values) if values else 0
        left_pad = 55
        bottom_pad = 45
        top_pad = 15
        right_pad = 15
        chart_w = w - left_pad - right_pad
        chart_h = h - bottom_pad - top_pad
        val_range = max_val - min_val if max_val != min_val else 1

        for i in range(5):
            y = top_pad + chart_h - (chart_h * i / 4)
            val = min_val + (max_val - min_val) * i / 4
            canvas.create_line(left_pad, y, w - right_pad, y, fill="#E0E0E0", dash=(2, 2))
            canvas.create_text(left_pad - 5, y, text=f"{val:,.0f}", anchor="e",
                               font=("Arial", 8), fill="#7F8C8D")

        points = []
        for i, (label, val) in enumerate(zip(labels, values)):
            x = left_pad + (chart_w * i / (n - 1)) if n > 1 else left_pad + chart_w / 2
            y = top_pad + chart_h - ((val - min_val) / val_range) * chart_h
            points.append((x, y))
            canvas.create_text(x, top_pad + chart_h + 8, text=str(label)[:10],
                               anchor="n", font=("Arial", 8), fill="#2C3E50")

        for i in range(len(points) - 1):
            canvas.create_line(points[i][0], points[i][1], points[i + 1][0], points[i + 1][1],
                               fill=color, width=2)

        for x, y in points:
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=color, outline="white")

    canvas.bind("<Configure>", draw_chart)
    chart_wrap.after(100, lambda: draw_chart())
    return frame