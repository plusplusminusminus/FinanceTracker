"""Dashboard window for navigating to other windows and viewing visual reports"""
import tkinter as tk
from idlelib.debugger_r import frametable
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.pyplot import figure
from sqlalchemy.testing.provision import temp_table_keyword_args

from .base_window import MainWindow

class DashboardWindow(MainWindow):
    """Main dashboard window with navigation and visual reports."""
    def __init__(self, app):
        super().__init__(app)
        self.daily_report_data = app.get_daily_report_data()
        self.weekly_report_data = app.get_weekly_report_data()
        self.monthly_report_data = app.get_monthly_report_data()
        self.root.title("Dashboard Window")
        self.root.geometry("400x400")
        #self.center_window(self.root.winfo_width(), self.root.winfo_height()) # Center the window

        nav_bar = tk.Frame(self.root)
        nav_bar.pack(fill="x", pady=10)
        tk.Button(nav_bar, text="Input Transactions", command=self.open_input_transaction).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Transaction History", command=self.open_transaction_history).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Goals", command=self.open_goals).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Account", command=self.open_account).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Sign Out", command=self.sign_out).pack(side="right", padx=6)

        self.display_summary()

        self.root.mainloop()

    def open_input_transaction(self):
        """Open the input transaction window."""
        from .input_transaction_window import InputTransactionWindow
        
        self.root.destroy()
        InputTransactionWindow(self.app)

    def open_transaction_history(self):
        """Open the transaction history window."""
        from .transaction_history_window import TransactionHistoryWindow
        
        self.root.destroy()
        TransactionHistoryWindow(self.app)

    def open_goals(self):
        """Open the goals window."""
        from .goals_window import GoalsWindow
        
        self.root.destroy()
        GoalsWindow(self.app)

    def open_account(self):
        """Open the account window."""
        from .account_window import AccountWindow
        
        self.root.destroy()
        AccountWindow(self.app)

    def display_summary(self):
        """Display the charts.""" """ Pie charts showing expenses and income by category """

        expenses = self.monthly_report_data["expenses_by_category"]
        categories = []
        amounts = []
        sizes = []

        for category, amount in expenses.items():
            categories.append(category)
            amounts.append(amount)

        for i in range(len(categories)):
            sizes.append(amounts[i] * 100 / sum(amounts))

        fig = Figure(figsize=(3, 3), dpi=100)
        ax = fig.add_subplot(1, 1, 1)

        ax.pie(sizes, labels=categories, autopct='%1.1f%%', startangle=140, pctdistance=0.5, labeldistance=1.5)

        ax.axis("equal")
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def sign_out(self):
        """Sign out and return to login window."""
        from .login_window import LoginWindow
        
        self.app.session_manager.logout()
        self.root.destroy()
        LoginWindow(self.app)