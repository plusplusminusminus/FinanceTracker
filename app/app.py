from database.db_config import SessionLocal, Base, engine
from database.crud.category_crud import CategoryCrud
from database.crud.user_crud import UserCrud
from client.windows.base_window import MainWindow
from app.sessions import SessionManager
from app.authentication import Authentication
from app.goals import Goals
from app.transactions import Transactions

from client.windows.login_window import LoginWindow

class FinanceApp:
    def __init__(self):
        self._initialize_database()
        self._db = SessionLocal()
        self._session_manager = SessionManager()
        self._authentication = Authentication(self._db)
        self._goals = Goals(self._db)
        self._user_crud = UserCrud(self._db)
        self._transactions = Transactions(self._db)
        self._category_crud = CategoryCrud(self._db)

        self.main_window = LoginWindow(self)

    def _initialize_database(self):
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()
        try:
            category_crud = CategoryCrud(session)
            category_crud.initialize_categories()
            print("Database initialized successfully")
        except Exception as e:
            print(f"Error initializing database: {e}")
            session.rollback()
        finally:
            session.close()

    @property
    def session_manager(self):
        return self._session_manager

    @property
    def authentication(self):
        return self._authentication

    @property
    def goals(self):
        return self._goals

    @property
    def transactions(self):
        return self._transactions

    @property
    def category_crud(self):
        return self._category_crud

    def login(self, email, password):
        user = self._user_crud.authenticate_user(email, password)
        if user:
            print(user.username)
            self._session_manager.login(user)
            return user
        else:
            print("Invalid credentials")
            return None

    def close(self):
        if self._db:
            self._db.close()
        self._session_manager.clear()