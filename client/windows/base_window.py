"""Base window class for the rest of the windows."""
import tkinter as tk


class MainWindow:
    """Base class for the rest of the windows."""
    def __init__(self, app):
        """Initialize the base window."""
        self.app = app
        self.root = tk.Tk()
        # close the app and destroy the window when the user click on the x button to close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Close the app and destroy the window when user close the window."""
        try:
            self.app.close()
        finally:
            self.root.destroy()

