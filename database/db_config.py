from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine=create_engine("sqlite:///finance_tracker.db")
Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

