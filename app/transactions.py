from datetime import datetime

from database.db_config import SessionLocal
from database_branch.database.crud import transaction_crud

class TransactionService:
    def __init__(self):
        self._db = SessionLocal()

    def add_expense(self, user_id: int, category_id: int, amount: float, description: str = None):
        return transaction_crud.create_transaction(self._db, user_id, category_id, amount, "expense", description)

    def add_income(self, user_id: int, category_id: int, amount: float, description: str = None):
        return transaction_crud.create_transaction(self._db, user_id, category_id, amount, "income", description)

    def get_transaction_by_id(self, user_id: int, transaction_id: int):
        return transaction_crud.get_transaction_by_id(transaction_id, user_id)

    def get_transactions_by_type(self, user_id: int, transaction_type: str):
        return transaction_crud.get_transaction_by_type(user_id, transaction_type)

    def get_transactions_by_category(self, user_id: int, category_id: int):
        return transaction_crud.get_transaction_by_category(user_id, category_id)

    def get_transactions_by_date(self, user_id: int, date: datetime):
        return transaction_crud.get_transaction_by_date(user_id, date)

    def get_user_transactions(self, user_id: int):
        return transaction_crud.get_transaction_by_user(self._db, user_id)

    def get_expense_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return transaction_crud.get_expense_by_category(user_id, start_date, end_date)

    def get_income_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return transaction_crud.get_income_by_category(user_id, start_date, end_date)

    # for debugging
    def print_all_transactions(self, user_id: int):
        txs = self.get_user_transactions(user_id)
        print("\n=== TRANSACTIONS FOR USER", user_id, "===\n")
        for tx in txs:
            print(
                f"ID: {tx.id} | "
                f"Type: {tx.type} | "
                f"Category: {tx.category_id} | "
                f"Amount: {tx.amount} | "
                f"Description: {tx.description} | "
                f"Created: {tx.created_on}"
            )
        print("=====================================\n")
