from database.db_config import Base, engine, SessionLocal
from database.models import user_model, category_model, goal_model, transaction_model
from datetime import date
from database.crud import user_crud_using_hashlib

Base.metadata.create_all(bind=engine)

db = SessionLocal()

user_crud_using_hashlib.create_user(db, "alex", "alex@example.com", "12345", date(1990, 1, 1))

hashed_password = user_crud_using_hashlib.hash_password("12345")

other_hashed_password = user_crud_using_hashlib.hash_password("12345")

another_hashed_password = user_crud_using_hashlib.hash_password("12345")

print(hashed_password)
print(other_hashed_password)
print(another_hashed_password)
