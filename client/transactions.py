import tkinter as tk
from tkinter import ttk

class SimpleInputDialog(tk.Toplevel):
    def __init__(self, parent, title="Enter Value", prompt="Please enter text:", initial_text=""):
        super().__init__(parent)
        self.parent = parent
        self.result = None
        self.title(title)
        self.transient(parent)
        self.grab_set()  # make modal

        title_lbl = ttk.Label(self, text=title, font=("TkDefaultFont", 14, "bold"))
        title_lbl.pack(padx=12, pady=(12, 6))

        prompt_lbl = ttk.Label(self, text=prompt)
        prompt_lbl.pack(padx=12, anchor="w")

        self.text_var = tk.StringVar(value=initial_text)
        self.text_box = ttk.Entry(self, textvariable=self.text_var, width=50)
        self.text_box.pack(padx=12, pady=6, fill="x")
        self.text_box.focus_set()

        # Button frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(padx=12, pady=(6, 12), fill="x")

        ok_btn = ttk.Button(btn_frame, text="OK", command=self.on_ok)
        ok_btn.pack(side="right")
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.on_cancel)
        cancel_btn.pack(side="right", padx=(0, 6))

        # Bind Enter/Escape
        self.bind("<Return>", lambda e: self.on_ok())
        self.bind("<Escape>", lambda e: self.on_cancel())

        # Center dialog over parent
        self.update_idletasks()
        x = parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

    def on_ok(self):
        self.result = self.text_var.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

# Example
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # hide main window for now

    dlg = SimpleInputDialog(root, title="Insert Financial Note", prompt="Enter line item description or note:",
                        initial_text="Revenue - Product A")
    root.wait_window(dlg)
    print("Test result:", dlg.result)
    root.destroy()