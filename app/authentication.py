from sqlalchemy.orm import Session
from database.crud.user_crud import UserCrud
from datetime import date

class Authentication:
    def __init__(self, db: Session):
        self._db = db
        self._user_crud = UserCrud(db)

    def login(self, email: str, password: str):
        if not email or not password:
            return False, None, "Email and password are required"
        try:
            user = self._user_crud.authenticate_user(email, password)
            if user:
                return True, user, "Loging successful"
            else:
                return False, None, "Invalid login credentials"
        except Exception as e:
            return False, None, f"Error logging in: {e}"

    def register(self, username: str, email: str, password: str, birthdate: date = None):
        if not username or not email or not password:
            return False
        # check to see if password is less than characters
        if (len(password) < 5):
            return False, "Password have to be longer than 5 characters"

        # check if email already exists
        try:
            existing_email = self._user_crud.get_user_by_email(email)
            if existing_email:
                return False, "Email already exists"
        except Exception as e:
            return False, f"Eror checking for existing email: {e}"

        # create the user
        try:
            user = self._user_crud.create_user(username, email, password, birthdate)
            if user:
                return True, "User created sucessfully"
        except Exception as e:
            return False, f"Error creating user: {e}"

    def logout(self):
        return True, "Logout successful"
