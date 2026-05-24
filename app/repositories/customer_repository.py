from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(
        self,
        email: str,
    ) -> Optional[Customer]:
        stmt = select(Customer).where(
            Customer.cliente_email == email
        )

        return self.db.scalar(stmt)

    def save(
        self,
        customer: Customer,
    ) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)

        return customer

    def update(
        self,
        customer: Customer,
    ) -> Customer:
        merged = self.db.merge(customer)

        self.db.commit()
        self.db.refresh(merged)

        return merged