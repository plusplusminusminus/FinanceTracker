import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class MainWindow:
    def __init__(self, on_login, on_csv_upload):
        # Create the main window
        self.window = tk.Tk()
        self.window.title("FinanceTracker Login")
        self.window.geometry("400x400")
        self.on_login = on_login
        self.on_csv_upload = on_csv_upload
    # if self.on_csv_upload():
    #     #messagebox.showinfo(title="Login Success", message="You successfully logged in.")
    # else:
    #     #messagebox.showerror(title="Error", message="Invalid login.")

        # Upload CSV function
        def upload():
            file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            self.on_csv_upload(file_path)
        # Upload CSV
        self.upload_csv = ttk.Button(self.window, text="Uploading the CSV", command=upload)
        self.upload_csv.pack(pady=10)

        # Title label
        title_label = ttk.Label(self.window, text="Login", font=("Arial", 16))
        title_label.pack(pady=10)

        # Username label and entry
        email_label = ttk.Label(self.window, text="Email", font=("Arial", 16))
        email_label.pack(pady=5)
        email_value = tk.StringVar()
        email_entry = tk.Entry(self.window, textvariable=email_value, width=30)
        email_entry.pack(padx=10, pady=10)

        # Password label and entry
        password_label = ttk.Label(self.window, text="Password", font=("Arial", 16))
        password_label.pack(pady=5)
        password_value = tk.StringVar()
        password_entry = tk.Entry(self.window, textvariable=password_value, width=30)
        password_entry.pack(padx=10, pady=10)

        # Login function
        def login():
            email = email_entry.get()
            password = password_entry.get()

            if self.on_login(email, password):
                messagebox.showinfo(title="Login Success", message="You successfully logged in.")
            else:
                messagebox.showerror(title="Error", message="Invalid login.")

        # Button to trigger login
        login_button = ttk.Button(self.window, text="Login", command=login)
        login_button.pack(pady=10)

        def open_main_screen():
            pass

    def show(self):
        self.window.mainloop()