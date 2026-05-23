from sqlalchemy import Column, Integer, String, Numeric
from app.database.connection import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    type_event = Column(String(255), nullable=False)
    equity_value = Column(Numeric(15, 2), nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(50), nullable=True)