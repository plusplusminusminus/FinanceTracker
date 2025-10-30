from sqlalchemy import Column, Integer, String
from database.db_config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True,index = True)
    email = Column(String, unique= True, nullable = False)
    password = Column(String, nullable = True)
