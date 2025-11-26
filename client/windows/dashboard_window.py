"""Dashboard window for navigating to other windows and viewing visual reports"""
import tkinter as tk
from tkinter import ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from .base_window import MainWindow
from .input_transaction_window import InputTransactionWindow
from .transaction_history_window import TransactionHistoryWindow
from .goals_window import GoalsWindow
from .account_window import AccountWindow
from .login_window import LoginWindow

class DashboardWindow(MainWindow):
    """Main dashboard window with navigation and visual reports."""
    def __init__(self, app):
        super().__init__(app)
        self.daily_report_data = app.get_daily_report_data()
        self.weekly_report_data = app.get_weekly_report_data()
        self.monthly_report_data = app.get_monthly_report_data()
        self.root.title("Dashboard Window")
        self.root.geometry("700x700")
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
        self.root.destroy()
        InputTransactionWindow(self.app)

    def open_transaction_history(self):
        """Open the transaction history window."""
        self.root.destroy()
        TransactionHistoryWindow(self.app)

    def open_goals(self):
        """Open the goals window."""
        self.root.destroy()
        GoalsWindow(self.app)

    def open_account(self):
        """Open the account window."""
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
        else:
            raise RuntimeError("Invalid selection")

        final_expense_categories, final_expense_sizes = self.create_chart_data(expenses)
        final_income_categories, final_income_sizes = self.create_chart_data(incomes)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text="Expenses")
        notebook.add(tab2, text="Incomes")
        self.create_pie_and_bar_charts(tab1, final_expense_sizes, final_expense_categories)
        self.create_pie_and_bar_charts(tab2, final_income_sizes, final_income_categories)

    def create_pie_and_bar_charts(self, parent, data, labels):
        """Create the pie-and-bar charts."""
        for child in parent.winfo_children():
            child.destroy()

        fig = Figure(figsize=(5, 5), dpi=100)
        axes = fig.subplots(1, 2)
        ax_pie = axes[0]
        ax_bar_chart = axes[1]
        ax_pie.pie(data, labels=None, autopct='%1.1f%%', startangle=140, pctdistance=0.5, labeldistance=1.5)
        ax_pie.legend(labels, loc='upper right')
        ax_pie.axis('equal')
        ax_bar_chart.bar(labels, data)
        fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, parent)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def create_chart_data(self, data):
        """Create the chart data."""
        final_categories = []
        final_sizes = []
        other = 0
        other_cutoff = 5
        amount_sum = sum(data.values())

        for category, amount in data.items():
            percents = amount * 100 / amount_sum
            if percents > other_cutoff:
                final_categories.append(category)
                final_sizes.append(amount)
            else:
                other += amount
        if other > 0:
            final_categories.append("Other")
            final_sizes.append(other)

        return final_categories, final_sizes

    def display_summary(self):
        """Display the charts."""
        self.time_frame = ["daily", "weekly", "monthly"]
        self.selected_time_frame = tk.StringVar(value=self.time_frame[2])
        tk.OptionMenu(self.root, self.selected_time_frame, *self.time_frame).pack(pady=6)
        self.selected_time_frame.trace_add("write", lambda *args: self.update_graph())
        self.update_graph()

    def sign_out(self):
        """Sign out and return to login window."""
        self.app.session_manager.logout()
        self.root.destroy()
        LoginWindow(self.app)
