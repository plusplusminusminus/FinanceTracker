"""Test the CategoryCrud class."""

import pytest
from database.crud.category_crud import CategoryCrud
from database.models.category_model import Category

class TestCategoryCrud:
    """Test CategoryCrud database crud operations."""
    def test_initialize_categories(self, db_session):
        """Test initializing the categories."""
        category_crud = CategoryCrud(db_session)
        category_crud.initialize_categories()
        assert category_crud.get_category_by_name("Groceries") is not None

    def test_get_category_by_name(self, test_category, category_crud):
        """Test getting a category by name."""
        groceries_category = category_crud.get_category_by_name("Groceries")
        assert groceries_category is not None
        assert groceries_category.name == "Groceries"

    def test_get_all_categories(self, category_crud):
        """Test getting all categories."""
        category_crud.initialize_categories()
        all_categories = category_crud.get_all_categories()
        assert all_categories is not None
        assert len(all_categories) > 0
        assert len(all_categories) == len(CategoryCrud.CATEGORIES)
        for category in all_categories:
            assert category.name is not None
            assert category.name in CategoryCrud.CATEGORIES

    def test_get_nonexistent_category(self, category_crud, test_category):
        """Test getting a nonexistent categoy."""
        nonexistent_category = category_crud.get_category_by_name("Music")
        assert nonexistent_category is None