from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        customer: Customer
    ) -> Customer:

        self.db.add(customer)

        self.db.commit()

        self.db.refresh(customer)

        return customer

    def find_by_email(
        self,
        email: str
    ) -> Customer | None:

        return (
            self.db.query(Customer)
            .filter(Customer.cliente_email == email)
            .first()
        )

    def find_by_id(
        self,
        customer_id: int
    ) -> Customer | None:

        return (
            self.db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    def update(
        self,
        customer: Customer
    ) -> Customer:

        self.db.commit()

        self.db.refresh(customer)

        return customer