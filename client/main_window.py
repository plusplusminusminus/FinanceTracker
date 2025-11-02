import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class MainWindow:
    def __init__(self, on_login):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("FinanceTracker Login")
        self.window.geometry("200x200")
        self.on_login = on_login

        # Title label
        title_label = ttk.Label(self.window, text="Login", font=("Arial", 16))
        title_label.pack(pady=10)

        # Username label and entry
        username_label = ttk.Label(self.window, text="Username", font=("Arial", 16))
        username_label.pack(pady=5)
        username_value = tk.StringVar()
        username_entry = tk.Entry(self.window, textvariable=username_value, width=30)
        username_entry.pack(padx=10, pady=10)

        # Password label and entry
        password_label = ttk.Label(self.window, text="Password", font=("Arial", 16))
        password_label.pack(pady=5)
        password_value = tk.StringVar()
        password_entry = tk.Entry(self.window, textvariable=password_value, width=30)
        password_entry.pack(padx=10, pady=10)

        # Login function
        def login():
            username = username_entry.get()
            password = password_entry.get()

            if self.on_login(username, password):
                messagebox.showinfo(title="Login Success", message="You successfully logged in.")
            else:
                messagebox.showerror(title="Error", message="Invalid login.")

        # Button to trigger login
        login_button = ttk.Button(self.window, text="Login", command=login)
        login_button.pack(pady=10)

    def show(self):
        self.window.mainloop()