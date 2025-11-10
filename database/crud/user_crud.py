from sqlalchemy.orm import Session
from database.models.user_model import User
from passlib.context import CryptContext
from datetime import date

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Hash the password that hte user enter"""
def hash_password(password: str) -> str:
    return password_context.hash(password)

"""Verify the password that hte user enter with the hashed password"""
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

"""Create a new user with the hashed password"""
def create_user(db: Session, username: str, email: str, password: str, birthdate: date = none) -> User:
    hashed_pwd = hash_password(password)
    user = User(
        username=username,
        email=email,
        password = hashed_pwd,
        birthdate=birthdate
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

""""Return the user baed on their ID"""
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

"""Return the user based on their email"""
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

"""Return the user based on their username"""
def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

"""Return all of the users in the database"""
def get_all_users(db: Session) -> User:
    return db.query(User).all()

"""Delete the user based on thier ID"""
def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if not user:
        return False
    else:
        db.delete(user)
        db.commit()
        return True

"""Authenticate the user when logging in with email and password"""
def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user