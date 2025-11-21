"""Dashboard window for navigating to other windows and viewing visual reports"""
import tkinter as tk
from .base_window import MainWindow


class DashboardWindow(MainWindow):
    """Main dashboard window with navigation and visual reports."""
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Dashboard Window")
        self.root.geometry("400x400")

        nav_bar = tk.Frame(self.root)
        nav_bar.pack(fill="x", pady=10)
        tk.Button(nav_bar, text="Input Transactions", command=self.open_input_transaction).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Transaction History", command=self.open_transaction_history).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Goals", command=self.open_goals).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Account", command=self.open_account).pack(side="left", padx=6)
        tk.Button(nav_bar, text="Sign Out", command=self.sign_out).pack(side="right", padx=6)

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

    def sign_out(self):
        """Sign out and return to login window."""
        from .login_window import LoginWindow
        
        self.app.session_manager.logout()
        self.root.destroy()
        LoginWindow(self.app)

