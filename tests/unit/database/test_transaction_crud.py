"""Test TransactionCrud class"""

import pytest
from database.crud.transaction_crud import TransactionCrud
from database.models.transaction_model import Transaction
from datetime import date, datetime, timezone


class TestTransactionCrud:

    def test_create_transaction(self, test_user, test_category, category_crud, db_session):
        """Test creating a transaction."""
        transaction_crud = TransactionCrud(db_session)
        
        groceries_category = category_crud.get_category_by_name("Groceries")
        
        transaction = transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=50.0, type="expense", description="Weekly groceries")
    
        assert transaction is not None
        assert transaction.id is not None
        assert transaction.user_id == test_user.id
        assert transaction.category_id == groceries_category.id
        assert transaction.amount == 50.0
        assert transaction.type == "expense"
        assert transaction.description == "Weekly groceries"
        assert transaction.created_on is not None
    
    def test_get_transaction_by_id(self, test_user, test_transaction, transaction_crud):
        """Test getting transaction by its id and user id"""
        transaction = transaction_crud.get_transaction_by_id(test_transaction.id, test_user.id)

        assert transaction is not None
        assert transaction.id == test_transaction.id
        assert transaction.user_id == test_user.id
        assert transaction.amount == 100
        assert transaction.type == "income"

    def test_get_nonexistent_transaction_by_id(self, test_transaction, test_user, transaction_crud):
        """Test getting a nonexistent transaction by its id and user id"""
        invalid_user_id_transaction = transaction_crud.get_transaction_by_id(test_transaction.id, 20312)
        assert invalid_user_id_transaction is None
        
        invalid_transaction_id = transaction_crud.get_transaction_by_id(10, test_user.id)
        assert invalid_transaction_id is None
    
    def test_get_transaction_by_user(self, test_user, test_transaction, test_expense_transaction, transaction_crud):
        """Test getting transactions by user id"""
        transactions = transaction_crud.get_transaction_by_user(test_user.id)
        assert transactions is not None
        assert len(transactions) == 2
        assert transactions[0].id in [test_transaction.id, test_expense_transaction.id]
        assert transactions[1].id in [test_transaction.id, test_expense_transaction.id]
    
    def test_get_transaction_by_type(self, test_user, test_transaction, test_expense_transaction, transaction_crud):
        """Test getting transactions by type."""
        income_transactions = transaction_crud.get_transaction_by_type(test_user.id, "income")
        assert len(income_transactions) == 1
        assert income_transactions[0].id == test_transaction.id
        assert income_transactions[0].type == "income"
        
        expense_transactions = transaction_crud.get_transaction_by_type(test_user.id, "expense")
        assert len(expense_transactions) == 1
        assert expense_transactions[0].id == test_expense_transaction.id
        assert expense_transactions[0].type == "expense"
    
    def test_get_transaction_by_category(self, test_user, test_transaction, transaction_crud, category_crud):
        """Test getting transactions by category."""
        salary_category = category_crud.get_category_by_name("Salary")
        groceries_category = category_crud.get_category_by_name("Groceries")
        
        second_salary = transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=200.0, type="income", description="Bonus")
        
        salary_transactions = transaction_crud.get_transaction_by_category(test_user.id, salary_category.id)
        assert len(salary_transactions) == 2
        assert all(transaction.category_id == salary_category.id for transaction in salary_transactions)
        
        groceries_transactions = transaction_crud.get_transaction_by_category(test_user.id, groceries_category.id)
        assert len(groceries_transactions) == 0
    
    def test_get_transaction_by_date(self, test_user, test_income_transaction, test_expense_transaction, transaction_crud):
        """Test getting transactions by date range."""
        now = datetime.now(timezone.utc)
        
        # get all the transactions since no date is provided
        all_transactions = transaction_crud.get_transaction_by_date(test_user.id)
        assert len(all_transactions) >= 2
        
        # get only the transactions that the user made today
        today_date = datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=timezone.utc)
        today_transactions = transaction_crud.get_transaction_by_date(test_user.id, start_date=today_date)
        assert len(today_transactions) >= 1

    
    def test_delete_transaction(self, test_user, test_transaction, transaction_crud):
        """Test deleting a transaction."""
        transaction_id = test_transaction.id
        
        deleted_transaction = transaction_crud.delete_transaction(test_user.id, transaction_id)
        assert deleted_transaction is True
        
        retrieved_transaction = transaction_crud.get_transaction_by_id(transaction_id, test_user.id)
        assert retrieved_transaction is None
    
    def test_delete_transaction_nonexistent(self, test_user, transaction_crud):
        """Test deleting a nonexistent transaction."""
        deleted_transaction = transaction_crud.delete_transaction(test_user.id, 99999)
        assert deleted_transaction is False
    
    def test_get_total_transaction_by_type(self, test_user, transaction_crud, category_crud):
        """Test getting total transactions by type."""
        category_crud.initialize_categories()
        salary_category = category_crud.get_category_by_name("Salary")
        groceries_category = category_crud.get_category_by_name("Groceries")

        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=100.0, type="income", description="Salary 1")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=200.0, type="income", description="Salary 2")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=50.0, type="expense", description="Groceries 1")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=75.0, type="expense", description="Groceries 2")
        total_income = transaction_crud.get_total_transaction_by_type(test_user.id, "income", None, None)
        assert total_income == 300.0
        total_expense = transaction_crud.get_total_transaction_by_type(test_user.id, "expense", None, None)
        assert total_expense == 125.0
    
    def test_get_total_income(self, test_user, transaction_crud, category_crud):
        """Test getting total income."""
        category_crud.initialize_categories()
        salary_category = category_crud.get_category_by_name("Salary")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=500.0, type="income", description="Salary")
        transaction_crud.create_transaction(user_id=test_user.id,category_id=salary_category.id, amount=100.0, type="income", description="Salary 2")
        total_income = transaction_crud.get_total_income(test_user.id)
        assert total_income == 600.0  
    
    def test_get_total_expenses(self, test_user, transaction_crud, category_crud):
        """Test getting total expenses."""
        category_crud.initialize_categories()
        groceries_category = category_crud.get_category_by_name("Groceries")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=100.0, type="expense", description="Groceries")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=200.0, type="expense", description="Groceries 2")
        total_expenses = transaction_crud.get_total_expenses(test_user.id)
        assert total_expenses == 300.0
    
    def test_get_net_balance(self, test_user, transaction_crud, category_crud):
        """Test getting net balance."""
        category_crud.initialize_categories()
        salary_category = category_crud.get_category_by_name("Salary")
        groceries_category = category_crud.get_category_by_name("Groceries")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=1000.0, type="income", description="Salary")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=300.0, type="expense", description="Groceries")
        
        net_balance = transaction_crud.get_net_balance(test_user.id)
        assert net_balance is not None
        assert net_balance == 700.0
    
    def test_get_transactions_by_category(self, test_user, transaction_crud, category_crud):
        """Test getting transactions grouped by category."""
        category_crud.initialize_categories()
        salary_category = category_crud.get_category_by_name("Salary")
        groceries_category = category_crud.get_category_by_name("Groceries")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=100.0, type="income", description="Salary 1")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=200.0, type="income", description="Salary 2")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=50.0, type="expense", description="Groceries")
        
        income_by_category = transaction_crud.get_transactions_by_category(
            test_user.id, "income", None, None
        )
        assert "Salary" in income_by_category
        assert income_by_category["Salary"] == 300.0
        
        expense_by_category = transaction_crud.get_transactions_by_category(
            test_user.id, "expense", None, None
        )
        assert "Groceries" in expense_by_category
        assert expense_by_category["Groceries"] == 50.0
    
    def test_get_expense_by_category(self, test_user, transaction_crud, category_crud):
        """Test getting expenses by category."""
        category_crud.initialize_categories()
        groceries_category = category_crud.get_category_by_name("Groceries")
        transport_category = category_crud.get_category_by_name("Transport")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=groceries_category.id, amount=100.0, type="expense", description="Groceries")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=transport_category.id, amount=50.0, type="expense", description="Transport")
        
        expenses_by_category = transaction_crud.get_expense_by_category(test_user.id)
        assert "Groceries" in expenses_by_category
        assert "Transport" in expenses_by_category
        assert expenses_by_category["Groceries"] >= 100.0
        assert expenses_by_category["Transport"] >= 50.0
    
    def test_get_income_by_category(self, test_user, transaction_crud, category_crud):
        """Test getting income by category."""
        category_crud.initialize_categories()
        salary_category = category_crud.get_category_by_name("Salary")
        investment_category = category_crud.get_category_by_name("Investment")
        
        transaction_crud.create_transaction(user_id=test_user.id, category_id=salary_category.id, amount=1000.0, type="income", description="Salary")
        transaction_crud.create_transaction(user_id=test_user.id, category_id=investment_category.id, amount=500.0, type="income", description="Investment")
        
        income_by_category = transaction_crud.get_income_by_category(test_user.id)
        assert "Salary" in income_by_category
        assert "Investment" in income_by_category
        assert income_by_category["Salary"] == 1000.0
        assert income_by_category["Investment"] == 500.0
    
    def test_get_daily_report(self, test_user, test_income_transaction, test_expense_transaction, transaction_crud):
        """Test getting daily report."""
        daily_report = transaction_crud.get_daily_report(test_user.id)
        assert daily_report is not None
        assert isinstance(daily_report["date"], date)
        assert isinstance(daily_report["income"], float)
        assert isinstance(daily_report["expenses"], float)
        assert isinstance(daily_report["net_balance"], float)
        assert isinstance(daily_report["expenses_by_category"], dict)
        assert isinstance(daily_report["income_by_category"], dict)


    def test_get_weekly_report(self, test_user, test_income_transaction, test_expense_transaction, transaction_crud):
        """Test getting weekly report."""
        weekly_report = transaction_crud.get_weekly_report(test_user.id)
        assert weekly_report is not None
        assert isinstance(weekly_report["week_start"], date)
        assert isinstance(weekly_report["week_end"], date)
        assert isinstance(weekly_report["income"], float)
        assert isinstance(weekly_report["expenses"], float)
        assert isinstance(weekly_report["net_balance"], float)
        assert isinstance(weekly_report["expenses_by_category"], dict)
        assert isinstance(weekly_report["income_by_category"], dict)
    
    def test_get_monthly_report(self, test_user, test_income_transaction, test_expense_transaction, transaction_crud):
        """Test getting monthly report."""
        monthly_report = transaction_crud.get_monthly_report(test_user.id)
        assert monthly_report is not None
        assert isinstance(monthly_report["year"], int)
        assert isinstance(monthly_report["month"], int)
        assert isinstance(monthly_report["income"], float)
        assert isinstance(monthly_report["expenses"], float)
        assert isinstance(monthly_report["net_balance"], float)
        assert isinstance(monthly_report["expenses_by_category"], dict)
        assert isinstance(monthly_report["income_by_category"], dict)