from sqlalchemy.orm import Session
from database.models.category_model import Category

CATEGORIES = [
    "Shopping",
    "Transport",
    "Groceries",
    "Car Payment",
    "Credit Card Payment",
    "Rent/Mortgage",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Salary",
    "Investment",
    "Gift",
    "Other"
]

"""Initialize the categories if they dont exist in the category databse"""
def initialize_categories(db: Session) -> None:
    for category_name in CATEGORIES:
        exists = db.query(Category).filter(Category.name == category_name).first()
        if not exists:
            category = Category(name=category_name)
            db.add(category)
    db.commit()


def get_category_by_id(db: Session, id: int) -> Category:
    return db.query(Category).filter(Category.id == id).first()

def get_category_by_name(db:Session, name: str) -> Category:
    return db.query(Category).filter(Category.name == name).first()

def get_all_categories(db:Session) -> Category:
    return db.query(Category).all()
