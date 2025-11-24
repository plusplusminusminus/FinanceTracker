"""Fixtures for pytest testin"""

import pytest
from datetime import date
from unittest.mock import Mock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_config import Base
from database.crud.user_crud import UserCrud
from database.crud.goal_crud import GoalCrud
from database.crud.category_crud import CategoryCrud
from database.crud.transaction_crud import TransactionCrud

#=============================================================
#============FIXTURES FOR DATABASE TESTING====================
#=============================================================
@pytest.fixture
def db_session():
    """ Create in-memory SQLite database session for testing."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def user_crud(db_session):
    """Create a UserCrud instance for testing."""
    return UserCrud(db_session)

@pytest.fixture
def goal_crud(db_session):
    """Create a GoalCrud instance for testing."""
    return GoalCrud(db_session)

@pytest.fixture
def category_crud(db_session):
    """Create a CategoryCrud instance for testing."""
    return CategoryCrud(db_session)

@pytest.fixture
def transaction_crud(db_session):
    """Create a TransactionCrud instance for testing."""
    return TransactionCrud(db_session)

@pytest.fixture
def test_goal(test_user, db_session):
    """Create a test goal for testing."""
    goal_crud = GoalCrud(db_session)
    goal = goal_crud.create_goal(user_id=test_user.id, goal_description="Save for a new car", goal_amount=10000, current_amount=0, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31))
    return goal

@pytest.fixture
def test_category(db_session):
    """Create a test category for testing."""
    category_crud = CategoryCrud(db_session)
    category_crud.initialize_categories()

@pytest.fixture
def test_transaction(test_user, test_category, db_session):
    """Create a test transaction for testing."""
    transaction_crud = TransactionCrud(db_session)
    category_crud = CategoryCrud(db_session)
    salary_category = category_crud.get_category_by_name("Salary")
    transaction = transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=100, type="income", description="Salary")
    return transaction

@pytest.fixture
def test_income_transaction(test_user, test_category, db_session):
    """Create a test income transaction for testing."""
    transaction_crud = TransactionCrud(db_session)
    category_crud = CategoryCrud(db_session)
    salary_category = category_crud.get_category_by_name("Salary")
    transaction = transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=100.0,type="income", description="Salary")
    return transaction

@pytest.fixture
def test_expense_transaction(test_user, test_category, db_session):
    """Create a test expense transaction for testing."""
    transaction_crud = TransactionCrud(db_session)
    category_crud = CategoryCrud(db_session)
    groceries_category = category_crud.get_category_by_name("Groceries")
    transaction = transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=50.0, type="expense", description="Groceries")
    return transaction
@pytest.fixture
def test_user(db_session):
    """Create a test user for testing."""
    user_crud = UserCrud(db_session)
    user = user_crud.create_user(username="bob", email="bob@example.com", password="bob123", birthdate=date(2000, 1, 1))
    return user

#=============================================================
#============FIXTURES FOR BACKEND/APP TESTING=================
#=============================================================
@pytest.fixture
def mock_db():
    """Create a mock database session for testing."""
    return Mock()

@pytest.fixture
def mock_user_crud():
    """Create a mock UserCrud for testing."""
    return Mock()

@pytest.fixture
def mock_goal_crud():
    """Create a mock GoalCrud for testing."""
    return Mock()

@pytest.fixture
def mock_transaction_crud():
    """Create a mock TransactionCrud for testing."""
    return Mock()

@pytest.fixture
def mock_user():
    """Create a mock user object for testing."""
    mock_user = Mock()
    mock_user.id = 1
    mock_user.username = "bob"
    mock_user.email = "bob@example.com"
    return mock_user

@pytest.fixture
def mock_expense_transaction():
    """Create a mock transaction object for testing."""
    mock_transaction = Mock()
    mock_transaction.id = 1
    mock_transaction.amount = 50.0
    mock_transaction.description = "Groceries for the week"
    mock_transaction.type = "expense"
    mock_transaction.category_id = 2
    return mock_transaction

@pytest.fixture
def mock_income_transaction():
    """Create a mock income transaction object for testing."""
    mock_transaction = Mock()
    mock_transaction.id = 2
    mock_transaction.amount = 500.0
    mock_transaction.description = "Salary from job"
    mock_transaction.type = "income"
    mock_transaction.category_id = 3
    return mock_transaction

@pytest.fixture
def mock_goal():
    """Create a mock goal object for testing."""
    mock_goal = Mock()
    mock_goal.id = 1
    mock_goal.description = "Save for vacation trip"
    mock_goal.target_amount = 5000
    mock_goal.current_amount = 0
    mock_goal.status = "current"
    mock_goal.start_date = date(2025, 1, 1)
    mock_goal.end_date = date(2025, 12, 31)
    return mock_goal

