from sqlalchemy.orm import Session
from database.models.transaction_model import Transaction
from database.models.category_model import Category
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

class TransactionCrud:
    def __init__(self, db: Session):
        self._db = db

    def create_transaction(self, user_id: int, category_id: int, amount: float, type: str,
                        description: str = None) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            category_id=category_id,
            amount=amount,
            type=type,
            description=description
        )
        self._db.add(transaction)
        self._db.commit()
        self._db.refresh(transaction)
        return transaction


    def get_transaction_by_id(self, transaction_id: int, user_id: int) -> Transaction:
        return self._db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()


    def get_transaction_by_user(self, user_id: int) -> Transaction:
        return self._db.query(Transaction).filter(Transaction.user_id == user_id).all()


    def get_transaction_by_type(self, user_id: int, type: str) -> Transaction:
        return self._db.query(Transaction).filter(Transaction.type == type, Transaction.user_id == user_id).order_by(
            Transaction.created_on.desc()).all()


    def get_transaction_by_category(self, user_id: int, category_id: int) -> Transaction:
        return self._db.query(Transaction).filter(Transaction.user_id == user_id,
                                            Transaction.category_id == category_id).order_by(
            Transaction.created_on.desc()).all()


    def get_transaction_by_date(self, user_id: int, date: datetime) -> Transaction:
        return self._db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.created_on == date).order_by(
            Transaction.created_on.desc()).all()


    def update_transaction(self, transaction_id: int, user_id: int, amount: float = None, type: str = None,
                        description: str = None) -> Transaction:
        transaction = self.get_transaction_by_id(transaction_id, user_id)
        if not transaction:
            return None
        if amount is not None:
            transaction.amount = amount
        if type is not None:
            transaction.type = type
        if description is not None:
            transaction.description = description
        self._db.commit()
        self._db.refresh(transaction)
        return transaction


    """Delete a list of selected transaction for the user"""


    def delete_transaction(self, user_id: int, transaction_id: list[int]) -> int:
        transaction = self.get_transaction_by_id(transaction_id, user_id)
        delete_count = self._db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.id.in_(transaction_id)
            # filter the list of ID for the transaction being deleted and check if it exists
        ).delete(synchronize_session=False)

        self._db.commit()
        return delete_count


    """Get the total transaction by either "income" or "expense" and optionally filter within a date period"""


    def get_total_transaction_by_type(self, user_id: int, transaction_type: str, startdate: datetime,
                                    enddate: datetime) -> float:
        total_transaction = self._db.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.type == transaction_type
        )
        if startdate:
            total_transaction = total_transaction.filter(Transaction.created_on >= startdate)
        if enddate:
            total_transaction = total_transaction.filter(Transaction.created_on <= enddate)
        total_amount = total_transaction.scalar()
        if total_amount:
            return total_amount
        return 0.0


    """Helper method to get total income with optional start and end date"""


    def get_total_income(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> float:
        return self.get_total_transaction_by_type(user_id, "income", start_date, end_date)


    """Helper method to get total expense with optional start and end date"""


    def get_total_expenses(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> float:
        """Calculate total expenses for a user within an optional date range."""
        return self.get_total_transaction_by_type(user_id, "expense", start_date, end_date)


    """Get net balance for a user with optional start and end date"""


    def get_net_balance(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> float:
        income = self.get_total_income(user_id, start_date, end_date)
        expenses = self.get_total_expenses(user_id, start_date, end_date)
        return income - expenses


    """Get the transactions per categories"""


    def get_transactions_by_category(self, user_id: int, transaction_type: str, start_date: datetime,
                                    end_date: datetime) -> dict:
        # Get the total/sum amount of transaction for each category and label the column as "Total"
        # Filter by user id and type of transaction such as "income" or "expense"
        transaction_cats = self._db.query(
            Category.name,
            func.sum(Transaction.amount).label('Total')
        ).join(Transaction).filter(Transaction.user_id == user_id, Transaction.type == transaction_type)

        if start_date:
            transaction_cats = transaction_cats.filter(Transaction.created_on >= start_date)
        if end_date:
            transaction_cats = transaction_cats.filter(Transaction.created_on <= end_date)
        # Group all the transactions by the category name
        result = transaction_cats.group_by(Category.name)

        # Stores the transaction sum for each categories into a dicitonary
        totals_per_categories = {}
        for category, total in result:
            totals_per_categories[category] = float(total)

        return totals_per_categories


    """Get the expense based on every category"""


    def get_expense_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> dict:
        return self.get_transactions_by_category(user_id, "expense", start_date, end_date)


    """Get the income based on every category"""


    def get_income_by_category(self, user_id: int, start_date: datetime = None, end_date: datetime = None) -> dict:
        return self.get_transactions_by_category(user_id, "income", start_date, end_date)


    """Get the daily report from start to end of the day"""


    def get_daily_report(self, user_id: int, date: datetime = None) -> dict:
        if not date:
            date = datetime.now(timezone.utc)

        # get the start to end of day from 00:00:00 to 11:59:59
        start_of_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=timezone.utc)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)
        return {
            "date": date.date(),
            "income": self.get_total_income(user_id, start_of_day, end_of_day),
            "expenses": self.get_total_expenses(user_id, start_of_day, end_of_day),
            "net_balance": self.get_net_balance(user_id, start_of_day, end_of_day),
            "expenses_by_category": self.get_expense_by_category(user_id, start_of_day, end_of_day),
            "income_by_category": self.get_income_by_category(user_id, start_of_day, end_of_day)
        }


    """Get the weely report for the current week or any chosen week"""


    def get_weekly_report(self, user_id: int, date: datetime = None) -> dict:
        if not date:
            date = datetime.now(timezone.utc)

        # Get the start of the week on Monday 00:00:00
        start_of_week = date - timedelta(days=date.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

        # Get hte end of the week on Sunday 23:59:59
        end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

        return {
            "week_start": start_of_week.date(),
            "week_end": end_of_week.date(),
            "income": self.get_total_income(user_id, start_of_week, end_of_week),
            "expenses": self.get_total_expenses(user_id, start_of_week, end_of_week),
            "net_balance": self.get_net_balance(user_id, start_of_week, end_of_week),
            "expense_by_category": self.get_expense_by_category(user_id, start_of_week, end_of_week),
            "income_by_category": self.get_income_by_category(user_id, start_of_week, end_of_week)

        }


    """Get the montly report for current month or chosen month"""


    def get_monthly_report(self, user_id: int, year: int = None, month: int = None) -> dict:
        if not year or not month:
            now = datetime.now(timezone.utc)
            year = now.year
            month = now.month

        # Start of the month on the first day
        start_of_month = datetime(year, month, 1, tzinfo=timezone.utc)

        # End of the month on the last day
        # NOTE: If the month is 12, then the end of the month will be (year)-12-31 23:59:59
        if month == 12:
            end_of_month = datetime(year + 1, 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)
        else:
            end_of_month = datetime(year, month + 1, 1, tzinfo=timezone.utc) - timedelta(seconds=1)

        return {
            "year": year,
            "month": month,
            "income": self.get_total_income(user_id, start_of_month, end_of_month),
            "expenses": self.get_total_expenses(user_id, start_of_month, end_of_month),
            "net_balance": self.get_net_balance(user_id, start_of_month, end_of_month),
            "expenses_by_category": self.get_expense_by_category(user_id, start_of_month, end_of_month),
            "income_by_category": self.get_income_by_category(user_id, start_of_month, end_of_month)

        }
