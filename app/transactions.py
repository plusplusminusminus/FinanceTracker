from datetime import datetime
from sqlalchemy.orm import Session
from database.crud.transaction_crud import TransactionCrud

class Transactions:
    def __init__(self, db: Session):
        self._db = db
        self._transaction_crud = TransactionCrud(db)

    def add_expense(self, user_id: int, category_id: int, amount: float, description: str = None):
        return self._transaction_crud.create_transaction(user_id, category_id, amount, "expense", description)

    def add_income(self, user_id: int, category_id: int, amount: float, description: str = None):
        return self._transaction_crud.create_transaction(user_id, category_id, amount, "income", description)

    def get_transaction_by_id(self, user_id: int, transaction_id: int):
        return self._transaction_crud.get_transaction_by_id(transaction_id, user_id)

    def get_transactions_by_type(self, user_id: int, transaction_type: str):
        return self._transaction_crud.get_transaction_by_type(user_id, transaction_type)

    def get_transactions_by_category(self, user_id: int, category_id: int):
        return self._transaction_crud.get_transaction_by_category(user_id, category_id)

    def get_transactions_by_date(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return self._transaction_crud.get_transaction_by_date(user_id, start_date, end_date)

    def get_user_transactions(self, user_id: int):
        return self._transaction_crud.get_transaction_by_user(user_id)

    def get_expense_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return self._transaction_crud.get_expense_by_category(user_id, start_date, end_date)

    def get_income_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return self._transaction_crud.get_income_by_category(user_id, start_date, end_date)

    def get_daily_report_data(self, user_id: int, date: datetime = None):
        return self._transaction_crud.get_daily_report(user_id, date)

    def get_weekly_report_data(self, user_id: int, date: datetime = None):
        return self._transaction_crud.get_weekly_report(user_id, date)

    def get_monthly_report_data(self, user_id: int, start_date: datetime = None, end_date: datetime = None):
        return self._transaction_crud.get_monthly_report(user_id, start_date, end_date)

    def delete_user_transaction(self, user_id, transaction_id):
        try:
            deleted = self._transaction_crud.delete_transaction(user_id, transaction_id)
            if not deleted:
                return False, "Transaction not found"
            return True, "Deleted transaction successfully"
        except Exception as e:
            return False, f"Error deleting transaction: {e}"

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