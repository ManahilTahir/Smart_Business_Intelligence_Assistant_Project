"""
SettingsPage - Settings page for business configuration.
"""

import json
import os
import customtkinter as ctk
from tkinter import messagebox
from gui.components import create_section_header, create_button, COLORS, card_fg


class SettingsPage:
    """Settings page for business configuration."""

    SETTINGS_FILE = "settings.json"

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = ctk.CTkFrame(parent, fg_color="transparent")

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self._build_layout()

    def hide(self):
        self.frame.pack_forget()

    def _build_layout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        create_section_header(self.frame, "Settings",
                               "Configure business name, currency, and appearance")

        form_frame = ctk.CTkFrame(self.frame, fg_color=card_fg(), corner_radius=12,
                                  border_width=1, border_color=COLORS["border"])
        form_frame.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(form_frame, text="Business Configuration",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=(20, 10))

        name_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        name_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(name_frame, text="Business Name:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.name_entry = ctk.CTkEntry(name_frame, height=34, width=300,
                                       font=ctk.CTkFont(size=13))
        self.name_entry.insert(0, self.app.get_business_name())
        self.name_entry.pack(fill="x", pady=2)

        currency_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        currency_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(currency_frame, text="Currency:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.currency_combo = ctk.CTkComboBox(currency_frame, values=[
            "USD - $", "EUR - €", "GBP - £", "PKR - ₨", "INR - ₹",
            "AED - د.إ", "SAR - ﷼", "CAD - C$", "AUD - A$",
            "JPY - ¥", "CNY - ¥", "CHF - CHF", "TRY - ₺",
        ], height=34, width=200)
        current_cur = self.app.get_currency()
        from utils.helpers import Helpers
        cur_sym = Helpers.CURRENCY_SYMBOLS.get(current_cur, current_cur)
        self.currency_combo.set(f"{current_cur} - {cur_sym}")
        self.currency_combo.pack(anchor="w", pady=2)

        theme_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        theme_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(theme_frame, text="Theme Appearance:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.theme_combo = ctk.CTkComboBox(theme_frame, values=["Light", "Dark", "System"],
                                            height=34, width=150)
        current_theme = self.app.get_theme()
        self.theme_combo.set(current_theme)
        self.theme_combo.pack(anchor="w", pady=2)

        threshold_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        threshold_frame.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(threshold_frame, text="VIP Customer Threshold:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.vip_entry = ctk.CTkEntry(threshold_frame, height=34, width=150,
                                      font=ctk.CTkFont(size=13))
        self.vip_entry.insert(0, str(self.app.analyzer.vip_threshold))
        self.vip_entry.pack(anchor="w", pady=2)

        threshold_frame2 = ctk.CTkFrame(form_frame, fg_color="transparent")
        threshold_frame2.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(threshold_frame2, text="Regular Customer Threshold:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.regular_entry = ctk.CTkEntry(threshold_frame2, height=34, width=150,
                                          font=ctk.CTkFont(size=13))
        self.regular_entry.insert(0, str(self.app.analyzer.regular_threshold))
        self.regular_entry.pack(anchor="w", pady=2)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=20)
        create_button(btn_frame, "💾 Save Settings", self._save_settings,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "🔄 Reset to Defaults", self._reset_defaults,
                      fg_color=COLORS["warning"], hover_color="#E67E22").pack(side="left", padx=5)

        info_frame = ctk.CTkFrame(self.frame, fg_color=card_fg(), corner_radius=12,
                                   border_width=1, border_color=COLORS["border"])
        info_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(info_frame, text="About BusinessHub",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     text_color=COLORS["primary"]).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(info_frame,
                     text="A Python-based desktop Business Intelligence & Analytics application using OOP, Pandas, NumPy, and CustomTkinter.\n"
                          "No AI/ML is used. All insights are generated from rule-based data analysis.",
                     font=ctk.CTkFont(size=13),
                     text_color=COLORS["text_light"]).pack(anchor="w", padx=20, pady=(0, 15))

    def _save_settings(self):
        try:
            name = self.name_entry.get().strip()
            currency_display = self.currency_combo.get()
            currency = currency_display.split(" - ")[0].strip()
            theme = self.theme_combo.get()
            vip_threshold = float(self.vip_entry.get())
            regular_threshold = float(self.regular_entry.get())

            if not name:
                messagebox.showerror("Error", "Business name cannot be empty.")
                return

            self.app.set_business_name(name)
            self.app.set_currency(currency)
            self.app.set_theme(theme)
            self.app.analyzer.set_thresholds(vip_threshold, regular_threshold)

            self.app.save_settings()

            ctk.set_appearance_mode(theme)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Thresholds must be valid numbers.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")

    def _reset_defaults(self):
        if messagebox.askyesno("Confirm", "Reset all settings to defaults?"):
            self.app.set_business_name("BusinessHub")
            self.app.set_currency("PKR")
            self.app.set_theme("System")
            self.app.analyzer.set_thresholds(100000, 30000)
            self.app.save_settings()
            ctk.set_appearance_mode("System")
            self._build_layout()
            messagebox.showinfo("Success", "Settings reset to defaults.")