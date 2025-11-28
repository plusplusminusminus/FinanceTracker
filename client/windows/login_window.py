"""Login window for user authentication."""
import tkinter as tk
from tkinter import messagebox
from .base_window import MainWindow

class LoginWindow(MainWindow):
    """Window GUI and functions for user login."""
    def __init__(self, app):
        super().__init__(app)
        self.root.title("Login Window")
        self.root.geometry("400x400")
        self.center_window(900, 900)

        # Email label + entry
        tk.Label(self.root, text="Email").pack(anchor="w", padx=16, pady=(16, 2))
        self.email_value = tk.StringVar()
        tk.Entry(self.root, textvariable=self.email_value).pack(fill="x", padx=16)

        # Password label + entry
        tk.Label(self.root, text="Password").pack(anchor="w", padx=16, pady=(12, 2))
        self.password_value = tk.StringVar()
        tk.Entry(self.root, textvariable=self.password_value).pack(fill="x", padx=16)

        # Login function
        tk.Button(self.root, text="Login", command=self.on_login).pack(pady=12)
        tk.Button(self.root, text="Sign Up", command=self.open_sign_up_window).pack()

        self.root.mainloop()

    def on_login(self):
        """Login the user based on the details the entered."""
        from .dashboard_window import DashboardWindow
        
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
        """Open the sign up window for the user to sign up for an account."""
        from .signup_window import SignUpWindow
        
        self.root.destroy()
        SignUpWindow(self.app)

