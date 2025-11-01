import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.app import FinanceApp

# Initialize the FinanceApp backend
app = FinanceApp()

# Create the main window
window = tk.Tk()
window.title("FinanceTracker Login")
window.geometry("200x200")

# Title label
title_label = ttk.Label(window, text="Login", font=("Arial", 16))
title_label.pack(pady=10)

# Username label and entry
username_label = ttk.Label(window, text="Username", font=("Arial", 16))
username_label.pack(pady=5)
username_value = tk.StringVar()
username_entry = tk.Entry(window, textvariable=username_value, width=30)
username_entry.pack(padx=10, pady=10)

# Password label and entry
password_label = ttk.Label(window, text="Password", font=("Arial", 16))
password_label.pack(pady=5)
password_value = tk.StringVar()
password_entry = tk.Entry(window, textvariable=password_value, width=30)
password_entry.pack(padx=10, pady=10)

# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
    else:
        messagebox.showerror(title="Error", message="Invalid login.")

# Button to trigger login
login_button = ttk.Button(window, text="Login", command=login)
login_button.pack(pady=10)

window.mainloop()


