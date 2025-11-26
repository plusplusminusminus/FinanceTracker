"""Dashboard window for navigating to other windows and viewing visual reports"""
import tkinter as tk
from tkinter import ttk

from fontTools.varLib.mutator import percents
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

        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().pack()

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

    def update_graph(self):
        """Update the graph."""
        if self.selected_time_frame.get() == "daily":
            incomes = self.daily_report_data["income_by_category"]
            expenses = self.daily_report_data["expenses_by_category"]
        elif self.selected_time_frame.get() == "weekly":
            incomes = self.weekly_report_data["income_by_category"]
            expenses = self.weekly_report_data["expenses_by_category"]
        elif self.selected_time_frame.get() == "monthly":
            incomes = self.monthly_report_data["income_by_category"]
            expenses = self.monthly_report_data["expenses_by_category"]

        categories = []
        amounts = []

        final_categories = []
        final_sizes = []
        sizes = []
        other = 0
        other_cutoff = 5


        for category, amount in expenses.items():
            categories.append(category)
            amounts.append(amount)

        for i in range(len(categories)):
            percents = amounts[i] * 100 / sum(amounts)

            if percents > other_cutoff:
                final_categories.append(categories[i])
                final_sizes.append(amounts[i])
            else:
                other += amounts[i]

        if other > 0:
            final_categories.append("other")
            final_sizes.append(other)

        self.ax.clear()

        self.ax.pie(final_sizes, labels=None, autopct='%1.1f%%', startangle=140, pctdistance=0.5, labeldistance=1.5)

        self.ax.axis("equal")
        self.ax.legend(final_categories, loc="upper right")
        self.fig.tight_layout()
        self.canvas.draw()

    def display_summary(self):
        """Display the charts.""" """ Pie charts showing expenses and income by category """
        self.time_frame = ["daily", "weekly", "monthly"]

        self.selected_time_frame = tk.StringVar(value=self.time_frame[2])
        tk.OptionMenu(self.root, self.selected_time_frame, *self.time_frame).pack(pady=6)
        self.selected_time_frame.trace_add("write", lambda *args: self.update_graph())
        self.update_graph()
        # tk.Button(self.root, text="test", command=update_graph)
        # if self.selected_time_frame.get() == "daily":
        #     incomes = self.daily_report_data["income_by_category"]
        #     expenses = self.daily_report_data["expenses_by_category"]
        # elif self.selected_time_frame.get() == "weekly":
        #     incomes = self.weekly_report_data["income_by_category"]
        #     expenses = self.weekly_report_data["expenses_by_category"]
        # elif self.selected_time_frame.get() == "monthly":
        #     incomes = self.monthly_report_data["income_by_category"]
        #     expenses = self.monthly_report_data["expenses_by_category"]
        #
        # categories = []
        # final_categories = []
        # final_sizes = []
        # amounts = []
        # sizes = []
        # other = 0
        # other_cutoff = 5
        #
        # for category, amount in expenses.items():
        #     categories.append(category)
        #     amounts.append(amount)
        #
        # for i in range(len(categories)):
        #     percents = amounts[i] * 100 / sum(amounts)
        #
        #     if percents > other_cutoff:
        #         final_categories.append(categories[i])
        #         final_sizes.append(amounts[i])
        #     else:
        #         other += amounts[i]
        #
        # if other > 0:
        #     final_categories.append("other")
        #     final_sizes.append(other)
        #
        # fig = Figure(figsize=(5, 5), dpi=100)
        # ax = fig.add_subplot(1, 1, 1)
        #
        # ax.pie(final_sizes, labels=None, autopct='%1.1f%%', startangle=140, pctdistance=0.5, labeldistance=1.5)
        #
        # ax.axis("equal")
        # ax.legend(final_categories, loc="upper right")
        # fig.tight_layout()
        #
        # canvas = FigureCanvasTkAgg(fig, self.root)
        # canvas.draw()
        # canvas.get_tk_widget().pack()

    def sign_out(self):
        """Sign out and return to login window."""
        from .login_window import LoginWindow
        
        self.app.session_manager.logout()
        self.root.destroy()
        LoginWindow(self.app)

"""
bar chart with total income and total expenses

two bar charts (total income and total expenses) # like the male and female example in lecture

function for getting all of the income and expenses

same thing showing for daily, weekly, and monthly
"""