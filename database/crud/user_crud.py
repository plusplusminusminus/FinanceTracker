from sqlalchemy.orm import Session
from database.models.user_model import User
from datetime import date
from passlib.context import CryptContext

# import hashlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCrud:
    def __init__(self, db: Session):
        self._db = db

    """Hash the password that the user enters"""
    def hash_password(self, plain_text: str) -> bytes:
        # return hashlib.sha256(plain_text.encode()).hexdigest()
        return pwd_context.hash(plain_text)

    """Verify the password that hte user enter with the hashed password"""
    def verify_password(self, plain_password, hashed_password) -> bool:
        # return self.hash_password(plain_password) == hashed_password
        return pwd_context.verify(plain_password, hashed_password)

    """Create a new user with the hashed password"""
    def create_user(self, username: str, email: str, password: str, birthdate: date = None) -> User:
        hashed_pwd = self.hash_password(password)
        user = User(
            username=username,
            email=email,
            password = hashed_pwd,
            birthdate= birthdate
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    """"Return the user based on their ID"""
    def get_user_by_id(self, user_id: int) -> User:
        return self._db.query(User).filter(User.id == user_id).first()

    """Return the user based on their email"""
    def get_user_by_email(self, email: str) -> User:
        return self._db.query(User).filter(User.email == email).first()

    """Return the user based on their username"""
    def get_user_by_username(self, username: str) -> User:
        return self._db.query(User).filter(User.username == username).first()

    """Return all of the users in the database"""
    def get_all_users(self) -> User:
        return self._db.query(User).all()

    """Delete the user based on their ID"""
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        else:
            self._db.delete(user)
            self._db.commit()
            return True

    """Authenticate the user when logging in with email and password"""
    def authenticate_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user