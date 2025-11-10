from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database.db_config import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Relationships
    transactions = relationship("Transaction", back_populates="category")