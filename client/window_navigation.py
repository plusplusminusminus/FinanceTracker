import tkinter as tk
from tkinter import ttk, messagebox

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

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FinanceTracker Input and Categorize Expenses and Income")
        self.root.geometry("400x400")

        self.categories = [
            "Shopping", "Transport", "Groceries", "Car Payment", "Credit Card Payment",
            "Rent/Mortgage", "Utilities", "Entertainment", "Healthcare", "Education",
            "Salary", "Investment", "Gift", "Other"
        ]

        self.selected_category = tk.StringVar(value=self.categories[0])
        tk.OptionMenu(self.root, self.selected_category, *self.categories).pack()

        tk.Entry(self.root, width=40).pack()
        tk.Button(self.root, text="Submit", command=self.add_expense).pack()

        self.root.mainloop()


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