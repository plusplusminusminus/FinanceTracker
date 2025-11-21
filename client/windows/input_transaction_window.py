"""Input transaction window for adding income and expenses."""
import tkinter as tk
from tkinter import ttk, messagebox
from .base_window import MainWindow
from ..window_constants import INCOME_CATEGORIES, EXPENSE_CATEGORIES


class InputTransactionWindow(MainWindow):
    """Window GUI and functions for inputting income and expense transactions."""
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Input Expenses & Income")
        self.root.geometry("600x500")

        # Back button
        tk.Button(self.root, text="Back to Dashboard", command=self.return_back).pack(pady=8)

        # Create tabbed interface
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both")

        self.create_income_tab()
        self.create_expense_tab()

        self.notebook.add(self.income_frame, text="Income")
        self.notebook.add(self.expense_frame, text="Expenses")

        self.root.mainloop()

    def create_income_tab(self):
        """Create the income input tab for the user to input their income."""
        self.income_frame = tk.Frame(self.notebook)
        self.income_categories = list(INCOME_CATEGORIES)

        self.selected_income_category = tk.StringVar(value=self.income_categories[0])
        tk.OptionMenu(self.income_frame, self.selected_income_category, *self.income_categories).pack(pady=6)

        self.income_entry = tk.Entry(self.income_frame, width=30)
        self.income_entry.pack(pady=4)

        tk.Button(self.income_frame, text="Submit Income", command=self.add_income).pack(pady=4)

        self.tree = ttk.Treeview(self.income_frame, columns=("Amount"), show="tree headings", height=8)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=8)
        self.tree.heading("#0", text="Category")
        self.tree.heading("Amount", text="Amount")

    def add_income(self):
        """Add an income transaction for the user based on the details the entered."""
        category = self.selected_income_category.get()
        amount_str = self.income_entry.get().strip()
        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        current_user = self.app.session_manager.current_user
        if not current_user:
            messagebox.showerror("Error", "Need to be logged in to add transactions.")
            return

        # Get the category that the income is under so we can have a relationship where each transaction has a category
        category_obj = self.app.category_crud.get_category_by_name(category)
        if not category_obj:
            messagebox.showerror("Error", f"Category '{category}' not found.")
            return

        # Add the income that the user entered into the transaction database
        try:
            transaction = self.app.transactions.add_income(
                user_id=current_user.id,
                category_id=category_obj.id,
                amount=amount
            )
            messagebox.showinfo("Success", f"Added income: {category}, ${amount:.2f}")
            self.income_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add income: {str(e)}")

    def create_expense_tab(self):
        """Create the expense input tab for the user to input their expenses."""
        self.expense_frame = tk.Frame(self.notebook)
        self.expense_categories = list(EXPENSE_CATEGORIES)

        self.selected_expense_category = tk.StringVar(value=self.expense_categories[0])
        tk.OptionMenu(self.expense_frame, self.selected_expense_category, *self.expense_categories).pack(pady=6)

        self.expense_entry = tk.Entry(self.expense_frame, width=30)
        self.expense_entry.pack(pady=4)

        tk.Button(self.expense_frame, text="Submit Expense", command=self.add_expense).pack(pady=4)

    def add_expense(self):
        """Add an expense transaction for the user based on the details the entered."""
        category = self.selected_expense_category.get()
        amount_str = self.expense_entry.get().strip()
        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be greater than 0.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")
            return

        current_user = self.app.session_manager.current_user
        if not current_user:
            messagebox.showerror("Error", "Need to be logged in to add transactions.")
            return

        #Get the category that the expense is under so we can have a relationship where each transaction has a category
        category_obj = self.app.category_crud.get_category_by_name(category)
        if not category_obj:
            messagebox.showerror("Error", f"Category '{category}' not found.")
            return

        #Add the expense that the user entered into the transaction database
        try:
            transaction = self.app.transactions.add_expense(
                user_id=current_user.id,
                category_id=category_obj.id,
                amount=amount
            )
            messagebox.showinfo("Success", f"Added expense: {category}, ${amount:.2f}")
            self.expense_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

    def return_back(self):
        """Return to the dashboard window."""
        from .dashboard_window import DashboardWindow
        
        self.root.destroy()
        DashboardWindow(self.app)

