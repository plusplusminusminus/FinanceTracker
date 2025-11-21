from database.db_config import Base, engine, SessionLocal
from database.models.user_model import User
from database.models.category_model import Category
from database.models.goal_model import Goal
from database.models.transaction_model import Transaction

__all__ = [
    'Base',
    'engine', 
    'SessionLocal',
    'User',
    'Category',
    'Goal',
    'Transaction'
]


def initialize_database():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        initialize_categories(db)
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

