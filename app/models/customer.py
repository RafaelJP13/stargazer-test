from sqlalchemy import Column, Integer, String, Numeric
from app.database.connection import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nome = Column(String(255), nullable=False)
    cliente_email = Column(String(255), unique=True, nullable=False)
    tipo_solicitacao = Column(String(255), nullable=False)
    valor_patrimonio = Column(Numeric(15, 2), nullable=False)
    status = Column(String(50), nullable=False)
    prioridade = Column(String(50), nullable=True)