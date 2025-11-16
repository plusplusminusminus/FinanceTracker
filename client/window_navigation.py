import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

class MainWindow:
    def __init__(self, app):
        self.app = app
        self.root = tk.Tk()
        #close the app and destroy the window when the user click on the x button to close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)



    def on_close(self):
        try:
            self.app.close()
        finally:
            self.root.destroy()

class LoginWindow(MainWindow):
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Login Window")
        self.root.geometry("400x400")


        # Email label + entry
        tk.Label(self.root, text="Email").pack(anchor="w", padx=16, pady=(16,2))
        self.email_value = tk.StringVar()
        tk.Entry(self.root, textvariable=self.email_value).pack(fill="x", padx=16)


        # Password label + entry
        tk.Label(self.root, text="Password").pack(anchor="w", padx=16, pady=(12,2))
        self.password_value = tk.StringVar()
        tk.Entry(self.root, textvariable=self.password_value).pack(fill="x", padx=16)


        # Login function
        tk.Button(self.root, text="Login", command=self.on_login).pack(pady=12)
        tk.Button(self.root, text="Sign Up", command=self.open_sign_up_window).pack()

        self.root.mainloop()

    def on_login(self):
        email = self.email_value.get().strip()
        password = self.password_value.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "Email and password are required")
            return

        is_logged_in = self.app.login(email, password)
        if is_logged_in:
            self.root.destroy()
            DashboardWindow(self.app)
        else:
            messagebox.showerror("Error", "Invalid login credentials")
    
    def open_sign_up_window(self):
        self.root.destroy()
        SignUpWindow(self.app)

class SignUpWindow(MainWindow):
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Sign Up Window")
        self.root.geometry("400x400")
    
        self.username_value = tk.StringVar()
        self.email_value = tk.StringVar()
        self.password_value = tk.StringVar()
        self.birthdate_value = tk.StringVar()
        

        tk.Label(self.root, text="Username").pack(anchor="w", padx=16, pady=(16,2))
        tk.Entry(self.root, textvariable=self.username_value).pack(fill="x", padx=16)

        tk.Label(self.root, text="Email").pack(anchor="w", padx=16, pady=(10,2))
        tk.Entry(self.root, textvariable=self.email_value).pack(fill="x", padx=16)

        tk.Label(self.root, text="Password").pack(anchor="w", padx=16, pady=(10,2))
        tk.Entry(self.root, textvariable=self.password_value, show="*").pack(fill="x", padx=16)

        tk.Label(self.root, text="Birthdate (YYYY-MM-DD)").pack(anchor="w", padx=16, pady=(10,2))
        tk.Entry(self.root, textvariable=self.birthdate_value).pack(fill="x", padx=16)

        tk.Button(self.root, text = "Create Account", command=self.on_create_account).pack(pady=14)
        tk.Button(self.root, text = "Back to Sign In", command=self.return_back).pack()

        self.root.mainloop()

    def on_create_account(self):
        try:
            date = self.birthdate_value.get().strip()
            if date:
                birthdate = datetime.strptime(date, "%Y-%m-%d").date()
                username = self.username_value.get().strip()
                email = self.email_value.get().strip()
                password = self.password_value.get().strip()
                status, message = self.app.authentication.register(username, email, password, birthdate)
                if status:
                    messagebox.showinfo("Success", message)
                    self.return_back()
                else:
                    messagebox.showerror("Error", message)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def return_back(self):
        self.root.destroy()
        LoginWindow(self.app)

def DashboardWindow(MainWindow):
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Dashboard Window")
        self.root.geometry("400x400")

        self.root.mainloop()

# class InputExpensesWindow:
#     def add_expense(self):
#         pass

#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("FinanceTracker Input and Categorize Expenses and Income")
#         self.root.geometry("400x400")

#         self.categories = [
#             "Shopping", "Transport", "Groceries", "Car Payment", "Credit Card Payment",
#             "Rent/Mortgage", "Utilities", "Entertainment", "Healthcare", "Education",
#             "Salary", "Investment", "Gift", "Other"
#         ]

#         self.selected_category = tk.StringVar(value=self.categories[0])
#         tk.OptionMenu(self.root, self.selected_category, *self.categories).pack()

#         tk.Entry(self.root, width=40).pack()
#         tk.Button(self.root, text="Submit", command=self.add_expense).pack()

#         self.root.mainloop()


# class UserExpensesStats:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("FinanceTracker User Expense Stats")
#         self.root.geometry("400x400")

#         tk.Button(self.root, text="Input Expenses", command=self.open_input_expenses_window).pack()

#         self.root.mainloop()

#     def open_input_expenses_window(self):
#         self.root.destroy()
#         InputExpensesWindow()

