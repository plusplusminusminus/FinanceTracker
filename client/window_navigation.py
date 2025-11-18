import os
import tkinter as tk
from tkinter import ttk, messagebox, image_names
from PIL import Image, ImageTk

icon_directory = "icons"

icon_dictionary = {
    "Shopping": "shopping.png",
    "Transport": "transport.png",
    "Salary": "salary.png",
    "Credit Card Payment": "credit_card_payment.png"
    # "Groceries", "Car Payment", "Credit Card Payment",
    # "Rent/Mortgage", "Utilities", "Entertainment", "Healthcare", "Education",
    # "Gift", "Salary", "Investment", "Other"
}

def load_icon(category):
    path = os.path.join(icon_directory, icon_dictionary[category])
    path = os.path.abspath(path)

    try:
        print(path)
        IMG = Image.open(path).resize((16,16))
        return ImageTk.PhotoImage(IMG)
    except:
        print("Could not load icon")

class AmountEntry:
    def __init__(self, icon, category, amount):
        self.icon = icon
        self.category = category
        self.amount = amount


class MainWindow:
    def __init__(self, on_login):
        self.root = tk.Tk()
        self.login = on_login
        self.root.geometry("300x300")

        tk.Label(self.root, text="Main Window").pack()
        tk.Button(self.root, text="Login", command=self.open_login_window).pack()

        self.root.mainloop()

    def open_login_window(self):
        self.root.destroy()
        LoginWindow(self.login)

class InputExpensesWindow:
    def add_expense(self):
        pass

    def add_income(self):
        category = self.selected_income_category.get()
        amount = self.income_entry.get()
        print(category, amount)

    # one recent entries function
    # take type as a param

    def __init__(self):
        self.root = tk.Tk()
        self.past_entries = 4
        self.root.title("FinanceTracker Input and Categorize Expenses and Income")
        self.root.geometry("400x400")
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both') # Makes the notebook expand and fill the window
        self.create_income_tab()
        self.create_expense_tab()
        self.notebook.add(self.income_frame, text="Income Tab")
        self.notebook.add(self.expense_frame, text="Expense Tab")

        self.root.mainloop()

    def create_income_tab(self):
        self.income_categories = [
            "Salary", "Investment", "Other"
        ]

        self.income_frame = tk.Frame(self.notebook)

        self.selected_income_category = tk.StringVar(value=self.income_categories[0])
        tk.OptionMenu(self.income_frame, self.selected_income_category, *self.income_categories).pack()

        self.income_entry = (tk.Entry(self.income_frame, width=40))
        self.income_entry.pack()
        tk.Button(self.income_frame, text="Submit", command=self.add_income).pack()
        path = os.path.abspath("test_expenses.txt")
        tree = ttk.Treeview(self.income_frame, columns=("Amount"), show="tree headings", height=10)
        tree.pack(fill=tk.BOTH, expand=True)
        tree.heading("#0", text = "Category")
        tree.heading("Amount", text = "Amount")
        tree.column("#0", width=150)
        tree.column("Amount", width=150)
        entries = 0
        fallback_icon = ImageTk.PhotoImage(Image.open("/Users/tmoquin/Desktop/CS122/FinanceTracker-app-clean/icons/shopping.png").resize((16,16)))
        with open(path, "r") as f:
            for line in f.readlines():
                category, amount = line.split(",")
                entry = AmountEntry(load_icon(category), category, amount)
                # row = tk.Frame(self.income_frame).pack()
                # icon_label = ttk.Label(row, image=entry.icon).pack(side="left")
                # category_label = tk.Label(row, text=category).pack(side="left")
                # category_amount = tk.Label(row, text=amount).pack(side="left")
                entries += 1
                tree.insert("", tk.END, text=entry.category, image=fallback_icon, values=(entry.amount))
                if entries == self.past_entries:
                    break

        self.income_frame.pack()

    def create_expense_tab(self):
        self.expense_categories = [
            "Shopping", "Transport", "Groceries", "Car Payment", "Credit Card Payment",
            "Rent/Mortgage", "Utilities", "Entertainment", "Healthcare", "Education",
            "Gift", "Other"
        ]

        self.expense_frame = tk.Frame(self.notebook)

        self.selected_expense_category = tk.StringVar(value=self.expense_categories[0])
        tk.OptionMenu(self.expense_frame, self.selected_expense_category, *self.expense_categories).pack()

        tk.Entry(self.expense_frame, width=40).pack()
        tk.Button(self.expense_frame, text="Submit", command=self.add_expense).pack()

        self.expense_frame.pack()

class UserExpensesStats:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FinanceTracker User Expense Stats")
        self.root.geometry("400x400")

        tk.Button(self.root, text="Input Expenses", command=self.open_input_expenses_window).pack()

        self.root.mainloop()

    def open_input_expenses_window(self):
        self.root.destroy()
        InputExpensesWindow()


class LoginWindow:
    def __init__(self, on_login):
        self.root = tk.Tk()
        self.root.title("FinanceTracker Login")
        self.root.geometry("400x400")
        self.on_login = on_login

        tk.Label(self.root, text="Login Window").pack()

        # Title label
        ttk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        # Email label + entry
        ttk.Label(self.root, text="Email", font=("Arial", 16)).pack(pady=5)
        email_value = tk.StringVar()
        email_entry = tk.Entry(self.root, textvariable=email_value, width=30)
        email_entry.pack(padx=10, pady=10)

        # Password label + entry
        ttk.Label(self.root, text="Password", font=("Arial", 16)).pack(pady=5)
        password_value = tk.StringVar()
        password_entry = tk.Entry(self.root, textvariable=password_value, width=30)
        password_entry.pack(padx=10, pady=10)

        # Login function
        def login():
            email = email_value.get()
            password = password_value.get()

            if self.on_login(email, password):
                messagebox.showinfo("Login Success", "You successfully logged in.")
                self.open_user_expenses_stats()
            else:
                messagebox.showerror("Error", "Invalid login.")

        # Login button
        ttk.Button(self.root, text="Login", command=login).pack(pady=10)

        self.root.mainloop()

    def open_user_expenses_stats(self):
        self.root.destroy()
        UserExpensesStats()