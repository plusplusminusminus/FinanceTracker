"""Sign up window for new user sign up."""
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from .base_window import MainWindow


class SignUpWindow(MainWindow):
    """Window GUI and functions for user sign up."""
    def __init__(self, app):
        """Initialize the sign up window."""
        super().__init__(app)
        self.root.title("Sign Up Window")
        self.root.geometry("400x400")

        #self.center_window(self.root.winfo_width(), self.root.winfo_height())  # Center the window

        self.username_value = tk.StringVar()
        self.email_value = tk.StringVar()
        self.password_value = tk.StringVar()
        self.birthdate_value = tk.StringVar()

        tk.Label(self.root, text="Username").pack(anchor="w", padx=16, pady=(16, 2))
        tk.Entry(self.root, textvariable=self.username_value).pack(fill="x", padx=16)

        tk.Label(self.root, text="Email").pack(anchor="w", padx=16, pady=(10, 2))
        tk.Entry(self.root, textvariable=self.email_value).pack(fill="x", padx=16)

        tk.Label(self.root, text="Password").pack(anchor="w", padx=16, pady=(10, 2))
        tk.Entry(self.root, textvariable=self.password_value, show="*").pack(fill="x", padx=16)

        tk.Label(self.root, text="Birthdate (YYYY-MM-DD)").pack(anchor="w", padx=16, pady=(10, 2))
        tk.Entry(self.root, textvariable=self.birthdate_value).pack(fill="x", padx=16)

        tk.Button(self.root, text="Create Account", command=self.on_create_account).pack(pady=14)
        tk.Button(self.root, text="Back to Sign In", command=self.return_back).pack()

        self.root.mainloop()

    def on_create_account(self):
        """Create an account for the user based on the details the entered."""
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
        """Return to the login window."""
        from .login_window import LoginWindow
        
        self.root.destroy()
        LoginWindow(self.app)

