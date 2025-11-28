"""Account window for viewing account details."""
import tkinter as tk
from .base_window import MainWindow

class AccountWindow(MainWindow):
    """Window GUI and functions for viewing account details."""
    def __init__(self, app):
        """Initialize the account window."""
        super().__init__(app)

        self.root.title("Account Details Window")
        self.root.geometry("400x400")
        self.center_window(900, 900)

        self.account_details_frame = tk.LabelFrame(self.root, text="ACCOUNT DETAILS")
        self.account_details_frame.pack(fill="x", padx=16, pady=8)
        current_user = self.app.session_manager.current_user
        if current_user:
            tk.Label(self.account_details_frame, text="Username/Email:").pack(anchor="w", padx=16, pady=(16, 2))
            tk.Label(self.account_details_frame, text=f"{current_user.username} / {current_user.email}").pack(
                anchor="w", padx=16)
            tk.Label(self.account_details_frame, text="Birthdate:").pack(anchor="w", padx=16, pady=(10, 2))
            tk.Label(self.account_details_frame, text=f"{current_user.birthdate}").pack(anchor="w", padx=16)

        else:
            tk.Label(self.account_details_frame, text="No user logged in").pack(pady=16)

        tk.Button(self.root, text="Back to Dashboard", command=self.return_back).pack(pady=16)
        tk.Button(self.root, text="Sign Out", command=self.sign_out).pack(pady=16)

        self.root.mainloop()

    def return_back(self):
        """Return to the dashboard window."""
        from .dashboard_window import DashboardWindow
        
        self.root.destroy()
        DashboardWindow(self.app)

    def sign_out(self):
        """Sign out and return to login window."""
        from .login_window import LoginWindow
        
        self.app.session_manager.logout()
        self.root.destroy()
        LoginWindow(self.app)

