from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database.db_config import Base

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    status = Column(String, default="current")  #tracking status of the goal
    start_date= Column(Date, nullable=True)
    end_date= Column(Date, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="goals")