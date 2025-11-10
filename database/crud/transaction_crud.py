from sqlalchemy.orm import Session
from database.models.transaction_model import Transaction
from database.models.category_model import Category
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

def create_transaction(db: Session, user_id: int, category_id: int, amount: float, type: str, description: str = None) -> Transaction:
    transaction = Transaction(
        user_id = user_id,
        category_id = category_id,
        amount = amount,
        type = type,
        description = description
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transaction_by_id(db: Session , transaction_id: int, user_id: int) -> Transaction:
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

def get_transaction_by_user(db: Session, user_id: int) -> Transaction:
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()

def get_transaction_by_type(db: Session, user_id: int, type: str) -> Transaction:
    return db.query(Transaction).filter(Transaction.type == type, Transaction.user_id == user_id).order_by(Transaction.created_on.desc()).all()

def get_transaction_by_category(db: Session, user_id: int, category_id: int) -> Transaction:
    return db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.category_id == category_id).order_by(Transaction.created_on.desc()).all()

def get_transaction_by_date(db: Session, user_id: int, date: datetime) -> Transaction:
    return db.query(Transaction).filter(Transaction.user_id == user_id, Transaction.created_on == date).order_by(Transaction.created_on.desc()).all()

def update_transaction(db: Session, transaction_id: int, user_id: int, amount: float = None, type: str = None, description: str = None) -> Transaction:
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        return None
    if amount is not None:
        transaction.amount = amount
    if type is not None:
        transaction.type = type
    if description is not None:
        transaction.description = description
    db.commit()
    db.refresh(transaction)
    return transaction

"""Delete a list of selected transaction for the user"""
def delete_transaction(db: Session, user_id: int, transaction_id: list[int]) -> int:
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    delete_count = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.id.in_(transaction_id) #filter the list of ID for the transaction being deleted and check if it exists
    ).delete(synchronize_session=False)

    db.commit()
    return delete_count

def get_total_income():
    return

def get_total_expenses():
    return


