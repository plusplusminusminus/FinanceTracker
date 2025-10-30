from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from database.db_config import Base

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key= True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))