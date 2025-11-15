from database.db_config import SessionLocal
from database.crud.user_crud import UserCrud
from client.window_navigation import MainWindow
import pandas as pd

class FinanceApp:
    def __init__(self):
        self.db = SessionLocal()
        self.user_crud = UserCrud(self.db)
        self.main_window = MainWindow(self.login_user)

    def login_user(self, email, password):
        user = self.user_crud.authenticate_user(email, password)

        if user:
            print(user.username)
            return True
        else:
            print("Invalid credentials")
            return False

    def run(self):
        self.main_window.show()