from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository


def test_should_update_customer(db):
    repository = CustomerRepository(db)

    customer = Customer(
        cliente_nome="Rafael",
        cliente_email="rafael@email.com",
        tipo_solicitacao="Crédito",
        valor_patrimonio=100000,
        status="Pendente",
    )

    db.add(customer)
    db.commit()

    customer.status = "Processado"

    updated_customer = repository.update(customer)

    assert updated_customer.status == "Processado"

    persisted_customer = repository.get_by_email(
        "rafael@email.com"
    )

    assert persisted_customer.status == "Processado"