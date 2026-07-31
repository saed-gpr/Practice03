from core.database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Float


class Expense(Base):

    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()