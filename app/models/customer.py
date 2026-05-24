from decimal import Decimal
from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.database.connection import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    cliente_nome: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    cliente_email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    tipo_solicitacao: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    valor_patrimonio: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    prioridade: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )