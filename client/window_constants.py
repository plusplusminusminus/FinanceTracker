"""Constants and functions for icons, categories, and amount the user enter."""
import os
from PIL import Image, ImageTk

icon_directory = "icons"

icon_dictionary = {
    "Shopping": "shopping.png",
    "Transport": "transport.png",
    "Salary": "salary.png",
    "Credit Card Payment": "credit_card_payment.png",
    "Groceries": "groceries.png",
    "Car Payment": "car_payment.png",
    "Rent/Mortgage": "rent_mortgage.png",
    "Utilities": "utilities.png",
    "Entertainment": "entertainment.png",
    "Healthcare": "healthcare.png",
    "Education": "education.png",
    "Gift": "gift.png",
    "Investment": "investment.png",
    "Other": "other.png",
}

INCOME_CATEGORIES = ["Salary", "Investment", "Other"]

EXPENSE_CATEGORIES = [
    "Shopping", "Transport", "Groceries", "Car Payment", "Credit Card Payment",
    "Rent/Mortgage", "Utilities", "Entertainment", "Healthcare", "Education",
    "Gift", "Other"
]

def load_icon(category):
    """Load an icon from the icons dictionary that corresponds to the category."""
    path = os.path.join(icon_directory, icon_dictionary[category])
    path = os.path.abspath(path)

    try:
        print(path)
        IMG = Image.open(path).resize((16, 16))
        return ImageTk.PhotoImage(IMG)
    except:
        print("Could not load icon")


class AmountEntry:
    """Represents the user's input for an amount when inputting a transactionwith icon, category, and amount."""
    def __init__(self, icon, category, amount):
        self.icon = icon
        self.category = category
        self.amount = amount

