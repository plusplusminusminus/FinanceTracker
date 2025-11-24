"""Testing the Transactions class"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from app.transactions import Transactions

class TestTransactions:
    """Test Transactions functions and logic."""

    def test_add_expense_success(self, mock_db, mock_transaction_crud, mock_expense_transaction, mock_user):
        """Test adding an expense successfully"""
        mock_transaction_crud.create_transaction.return_value = mock_expense_transaction

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        #NOTE: I used randome int for user and category id since its just a mock unit test and we just want to test the function itslf
        result = transactions.add_expense(user_id=mock_user.id, category_id=2, amount=50.0, description="Groceries for the week")

        assert result == mock_expense_transaction
        mock_transaction_crud.create_transaction.assert_called_once_with(mock_user.id, 2, 50.0, "expense", "Groceries for the week")

    def test_add_income_success(self, mock_db, mock_transaction_crud, mock_income_transaction, mock_user):
        """Test adding an income successfully"""
        mock_transaction_crud.create_transaction.return_value = mock_income_transaction

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud

        result = transactions.add_income(user_id=mock_user.id, category_id=3, amount=500.0, description="Salary from job")

        assert result == mock_income_transaction
        mock_transaction_crud.create_transaction.assert_called_once_with(mock_user.id, 3, 500.0, "income", "Salary from job")
    
    def test_get_transaction_by_id_success(self, mock_db, mock_transaction_crud, mock_expense_transaction, mock_income_transaction, mock_user):
        """Test getting a transaction by its id for the user successfully"""
        #NOTE: the get_transaciton by id function in transactions.py is (user_i, transaction_id)
        #but the same fuunction in transaction_crud.py is (transaction_id, user_id)
        #so I just switched it around in this test but i dont think it matters
        mock_transaction_crud.get_transaction_by_id.side_effect = [mock_expense_transaction, mock_income_transaction]

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        result = transactions.get_transaction_by_id(mock_user.id, mock_expense_transaction.id)
        assert result == mock_expense_transaction
        mock_transaction_crud.get_transaction_by_id.assert_called_with(mock_expense_transaction.id, mock_user.id)

        result = transactions.get_transaction_by_id(mock_user.id, mock_income_transaction.id)
        assert result == mock_income_transaction
        assert mock_transaction_crud.get_transaction_by_id.call_count == 2
        mock_transaction_crud.get_transaction_by_id.assert_called_with(mock_income_transaction.id, mock_user.id) 

    def test_get_user_transactions_success(self, mock_db, mock_transaction_crud, mock_expense_transaction, mock_income_transaction, mock_user):
        """Test getting all transactions by the user id successfully"""
        mock_transaction_crud.get_transaction_by_user.return_value = [mock_expense_transaction, mock_income_transaction]

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        result = transactions.get_user_transactions(mock_user.id)
        assert result == [mock_expense_transaction, mock_income_transaction]
        mock_transaction_crud.get_transaction_by_user.assert_called_once_with(mock_user.id)

    def test_get_transactions_by_type_success(self, mock_db, mock_transaction_crud, mock_expense_transaction, mock_income_transaction, mock_user):
        """Test getting all transactions by the user id and the type successfully"""
        mock_transaction_crud.get_transaction_by_type.side_effect = [mock_expense_transaction, mock_income_transaction]

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        result = transactions.get_transactions_by_type(mock_user.id, "expense")
        assert result == mock_expense_transaction
        mock_transaction_crud.get_transaction_by_type.assert_called_once_with(mock_user.id, "expense")

        result = transactions.get_transactions_by_type(mock_user.id, "income")
        assert result == mock_income_transaction
        mock_transaction_crud.get_transaction_by_type.assert_called_with(mock_user.id, "income")
        assert mock_transaction_crud.get_transaction_by_type.call_count == 2


    def test_get_transactions_by_category_success(self, mock_db, mock_transaction_crud, mock_expense_transaction, mock_income_transaction, mock_user):
        """Test getting all transactions by the user id and the category id successfully"""
        mock_transaction_crud.get_transaction_by_category.side_effect = [mock_expense_transaction, mock_income_transaction]

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        result = transactions.get_transactions_by_category(mock_user.id, 2)
        assert result == mock_expense_transaction
        mock_transaction_crud.get_transaction_by_category.assert_called_once_with(mock_user.id, 2)
        assert result.description == mock_expense_transaction.description

        result = transactions.get_transactions_by_category(mock_user.id, 3)
        assert result == mock_income_transaction
        mock_transaction_crud.get_transaction_by_category.assert_called_with(mock_user.id, 3)
        assert result.description == mock_income_transaction.description
        assert mock_transaction_crud.get_transaction_by_category.call_count == 2

    def test_get_income_by_category(self, mock_db, mock_transaction_crud, mock_user):
        """Test getting the income of transactions by category"""
        expected_income_result = {"Salary": 500.0, "Investment": 200.0}
        mock_transaction_crud.get_income_by_category.return_value = expected_income_result

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        
        #test iwth no date and date sicne user might or might not want to have a daterange filter
        result = transactions.get_income_by_category(mock_user.id)
        assert result == expected_income_result
        mock_transaction_crud.get_income_by_category.assert_called_once_with(mock_user.id, None, None)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        result = transactions.get_income_by_category(mock_user.id, start_date, end_date)
        assert result == expected_income_result
        assert mock_transaction_crud.get_income_by_category.call_count == 2
        mock_transaction_crud.get_income_by_category.assert_called_with(mock_user.id, start_date, end_date)

    def test_get_expense_by_category(self, mock_db, mock_transaction_crud, mock_user):
        """Test getting the expenses of transactions by category"""
        expected_expense_result = {"Groceries": 150.0, "Shopping": 75.0, "Transport": 50.0}
        mock_transaction_crud.get_expense_by_category.return_value = expected_expense_result

        transactions = Transactions(mock_db)
        transactions._transaction_crud = mock_transaction_crud
        
        result = transactions.get_expense_by_category(mock_user.id)
        assert result == expected_expense_result
        mock_transaction_crud.get_expense_by_category.assert_called_once_with(mock_user.id, None, None)
        
        start_date = datetime(2025, 1, 1)
        end_date = datetime(2025, 12, 31)
        result = transactions.get_expense_by_category(mock_user.id, start_date, end_date)
        assert result == expected_expense_result
        assert mock_transaction_crud.get_expense_by_category.call_count == 2
        mock_transaction_crud.get_expense_by_category.assert_called_with(mock_user.id, start_date, end_date)