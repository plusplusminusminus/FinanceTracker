from sqlalchemy.orm import Session
from database.models.category_model import Category
from typing import Optional, List

class CategoryCrud:
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

    def __init__(self, db: Session):
        self._db = db

    """Initialize the categories if they dont exist in the category databse"""
    def initialize_categories(self) -> None:
        for category_name in self.CATEGORIES:
            exists = self._db.query(Category).filter(Category.name == category_name).first()
            if not exists:
                category = Category(name=category_name)
                self._db.add(category)
        self._db.commit()


    def get_category_by_id(self, id: int) -> Category:
        return self._db.query(Category).filter(Category.id == id).first()

    def get_category_by_name(self, name: str) -> Category:
        return self._db.query(Category).filter(Category.name == name).first()

    def get_all_categories(self) -> Category:
        return self._db.query(Category).all()
