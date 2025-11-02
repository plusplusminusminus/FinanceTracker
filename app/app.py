from client.main_window import MainWindow
from database.db_config import Database

class FinanceApp:
    def __init__(self):
        self.db = Database("financetracker.db")
        self.main_window = MainWindow(self.login_user)

    def login_user(self, username, password):
        result = self.db.query_user(username, password)

        if result:
            return True
        else:
            return False

    def run(self):
        self.main_window.show()