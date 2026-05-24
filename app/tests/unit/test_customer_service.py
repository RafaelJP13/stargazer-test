from decimal import Decimal

from sqlalchemy.orm import Session

from app.schemas.customer import CustomerCreateRequest
from app.services.customer_service import CustomerService


def test_create_customer(db: Session):
    service = CustomerService(db)

    payload = CustomerCreateRequest(
        cliente_nome="João Silva",
        cliente_email="joao@email.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=Decimal("250000.00")
    )

    customer = service.create(payload)

    assert customer.id is not None
    assert customer.cliente_nome == "João Silva"
    assert customer.cliente_email == "joao@email.com"
    assert customer.status == "Aguardando Análise"
    assert customer.prioridade is None


def test_get_customer_by_email(db: Session):
    service = CustomerService(db)

    payload = CustomerCreateRequest(
        cliente_nome="João Silva",
        cliente_email="joao@email.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=Decimal("250000.00")
    )

    created_customer = service.create(payload)

    customer = service.get_by_email("joao@email.com")

    assert customer is not None
    assert customer.id == created_customer.id
    assert customer.cliente_email == "joao@email.com"
    assert customer.cliente_nome == "João Silva"


def test_get_customer_by_email_not_found(db: Session):
    service = CustomerService(db)

    customer = service.get_by_email("naoexiste@email.com")

    assert customer is None


def test_update_status_and_priority(db: Session):
    service = CustomerService(db)

    payload = CustomerCreateRequest(
        cliente_nome="João Silva",
        cliente_email="joao@email.com",
        tipo_solicitacao="Atualização cadastral",
        valor_patrimonio=Decimal("250000.00")
    )

    customer = service.create(payload)

    updated_customer = service.update_status_and_priority(
        customer=customer,
        prioridade="prioridade_alta",
        card_id="card-123"
    )

    assert updated_customer.status == "Processado"
    assert updated_customer.prioridade == "prioridade_alta"

    persisted_customer = service.get_by_email("joao@email.com")

    assert persisted_customer is not None
    assert persisted_customer.status == "Processado"
    assert persisted_customer.prioridade == "prioridade_alta"