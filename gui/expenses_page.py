"""
ExpensesPage - Expense management page with CRUD operations.
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.components import (create_section_header, create_button, create_table,
                            create_search_bar, COLORS, card_fg)
from utils.validators import Validators
from utils.helpers import Helpers


class ExpensesPage:
    """Expense management page."""

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

        create_section_header(self.frame, "Expense Management",
                               "Add, edit, search, and manage expense records")

        top_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        top_frame.pack(fill="x", padx=20, pady=5)

        create_button(top_frame, "➕ Add Expense", self._open_add_form,
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(top_frame, "✏️ Edit Expense", self._open_edit_form,
                      fg_color=COLORS["warning"], hover_color="#E67E22").pack(side="left", padx=5)
        create_button(top_frame, "🗑️ Delete Expense", self._delete_expense,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

        filter_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        filter_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(filter_frame, text="Filter by Category:", font=ctk.CTkFont(size=13)).pack(side="left", padx=5)
        categories = ["All"] + self.app.expense_manager.get_categories()
        self.category_combo = ctk.CTkComboBox(filter_frame, values=categories, height=32, width=180,
                                                command=self._on_filter)
        self.category_combo.set("All")
        self.category_combo.pack(side="left", padx=5)

        create_search_bar(self.frame, self._on_search, "Search by category, description, date...")
        self._load_table()

    def _load_table(self, keyword="", category="All"):
        if hasattr(self, "table_frame"):
            self.table_frame.destroy()

        if keyword:
            df = self.app.expense_manager.search_expenses(keyword)
        else:
            df = self.app.expense_manager.get_all_expenses()

        if category and category != "All":
            df = df[df["Category"].astype(str) == str(category)] if not df.empty else df

        if df.empty:
            data = []
        else:
            currency = self.app.get_currency()
            data = []
            for _, row in df.iterrows():
                data.append({
                    "ExpenseID": row.get("ExpenseID", ""),
                    "Date": row.get("Date", ""),
                    "Category": row.get("Category", ""),
                    "Description": row.get("Description", ""),
                    "Amount": Helpers.format_currency(row.get("Amount", 0), currency),
                })

        self.table_frame = create_table(
            self.frame,
            ["ExpenseID", "Date", "Category", "Description", "Amount"],
            data,
        )

    def _on_search(self, keyword):
        self._load_table(keyword.strip(), self.category_combo.get())

    def _on_filter(self, choice):
        search_text = self.search_entry.get().strip() if hasattr(self, "search_entry") else ""
        self._load_table(search_text, choice)

    def _open_add_form(self):
        self._show_form_dialog("Add New Expense")

    def _open_edit_form(self):
        df = self.app.expense_manager.get_all_expenses()
        if df.empty:
            messagebox.showinfo("Info", "No expenses to edit.")
            return
        self._show_form_dialog("Edit Expense", is_edit=True)

    def _show_form_dialog(self, title, is_edit=False):
        dialog = ctk.CTkToplevel(self.frame)
        dialog.title(title)
        dialog.geometry("450x480")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=20, weight="bold"),
                     text_color=COLORS["primary"]).pack(pady=(20, 10))

        form_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)

        if is_edit:
            id_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            id_frame.pack(fill="x", pady=3)
            ctk.CTkLabel(id_frame, text="Expense ID to edit:", font=ctk.CTkFont(size=13)).pack(anchor="w")
            self.exp_id_entry = ctk.CTkEntry(id_frame, placeholder_text="Expense ID", height=32)
            self.exp_id_entry.pack(fill="x", pady=2)

            def load_expense():
                eid = self.exp_id_entry.get().strip()
                expense = self.app.expense_manager.get_expense_by_id(eid)
                if not expense:
                    messagebox.showerror("Error", "Expense not found.")
                    return
                self.date_entry.delete(0, "end")
                self.date_entry.insert(0, str(expense.get("Date", "")))
                self.cat_combo.set(str(expense.get("Category", "")))
                self.desc_entry.delete(0, "end")
                self.desc_entry.insert(0, str(expense.get("Description", "")))
                self.amount_entry.delete(0, "end")
                self.amount_entry.insert(0, str(expense.get("Amount", "")))

            create_button(id_frame, "Load", load_expense, width=70, height=30).pack(side="right", padx=5)

        date_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        date_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(date_frame, text="Date (YYYY-MM-DD):", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.date_entry = ctk.CTkEntry(date_frame, placeholder_text="YYYY-MM-DD", height=32)
        self.date_entry.insert(0, Helpers.today_string())
        self.date_entry.pack(fill="x", pady=2)

        cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        cat_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(cat_frame, text="Category:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.cat_combo = ctk.CTkComboBox(cat_frame, values=self.app.expense_manager.get_categories(), height=32)
        self.cat_combo.set("Rent")
        self.cat_combo.pack(fill="x", pady=2)

        desc_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        desc_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(desc_frame, text="Description:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.desc_entry = ctk.CTkEntry(desc_frame, placeholder_text="Enter description", height=32)
        self.desc_entry.pack(fill="x", pady=2)

        amount_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        amount_frame.pack(fill="x", pady=3)
        ctk.CTkLabel(amount_frame, text="Amount:", font=ctk.CTkFont(size=13)).pack(anchor="w")
        self.amount_entry = ctk.CTkEntry(amount_frame, placeholder_text="Enter amount", height=32)
        self.amount_entry.pack(fill="x", pady=2)

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=15)
        create_button(btn_frame, "Save", lambda: self._save_expense(dialog, is_edit),
                      fg_color=COLORS["success"], hover_color="#229954").pack(side="left", padx=5)
        create_button(btn_frame, "Cancel", dialog.destroy,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(side="left", padx=5)

    def _save_expense(self, dialog, is_edit):
        date = self.date_entry.get().strip()
        category = self.cat_combo.get().strip()
        description = self.desc_entry.get().strip()
        amount = self.amount_entry.get().strip()

        errors = Validators.validate_expense(date, category, description, amount)
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        try:
            if is_edit:
                eid = self.exp_id_entry.get().strip()
                if not eid:
                    messagebox.showerror("Error", "Please enter an Expense ID.")
                    return
                updated = {
                    "Date": date, "Category": category,
                    "Description": description, "Amount": float(amount),
                }
                self.app.expense_manager.update_expense(eid, updated)
                messagebox.showinfo("Success", "Expense updated successfully!")
            else:
                eid = self.app.expense_manager.add_expense(date, category, description, amount)
                messagebox.showinfo("Success", f"Expense added! ID: {eid}")

            dialog.destroy()
            self._load_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save expense: {e}")

    def _delete_expense(self):
        df = self.app.expense_manager.get_all_expenses()
        if df.empty:
            messagebox.showinfo("Info", "No expenses to delete.")
            return

        dialog = ctk.CTkToplevel(self.frame)
        dialog.title("Delete Expense")
        dialog.geometry("350x150")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Enter Expense ID to delete:", font=ctk.CTkFont(size=14)).pack(pady=20)
        id_entry = ctk.CTkEntry(dialog, placeholder_text="Expense ID", height=32, width=200)
        id_entry.pack(pady=5)

        def do_delete():
            eid = id_entry.get().strip()
            if not eid:
                messagebox.showerror("Error", "Please enter an Expense ID.")
                return
            if messagebox.askyesno("Confirm", f"Delete expense {eid}?"):
                self.app.expense_manager.delete_expense(eid)
                messagebox.showinfo("Success", "Expense deleted successfully!")
                dialog.destroy()
                self._load_table()

        create_button(dialog, "Delete", do_delete,
                      fg_color=COLORS["danger"], hover_color="#C0392B").pack(pady=10)