from decimal import Decimal
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerCreateRequest


def test_create_customer(db):

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