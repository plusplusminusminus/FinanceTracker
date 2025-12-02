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

    def center_window(self, width, height):
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_close(self, close_app=True):
        """Close the app and destroy the window when user close the entire window."""
        try:
            if close_app:
                self.app.close()
        finally:
            self.root.destroy()
    
    def close_window(self):
        """Close the window without closing the app whene user navigate through different windows."""
        self.on_close(close_app=False)

