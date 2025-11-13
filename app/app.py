from database.db_config import SessionLocal
from database.crud.user_crud_using_hashlib import authenticate_user
from client.window_navigation import MainWindow
import pandas as pd

class FinanceApp:
    def __init__(self):
        self.db = SessionLocal()
        self.main_window = MainWindow(self.login_user)

    def login_user(self, email, password):
        user = authenticate_user(self.db, email, password)

        if user:
            print(user.username)
            return True
        else:
            print("Invalid credentials")
            return False

    def run(self):
        self.main_window.show()