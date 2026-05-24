from decimal import Decimal

from app.models.customer import Customer
from app.services.webhook_service import WebhookService


def test_should_set_high_priority_when_patrimonio_is_exactly_200k(db):
    customer = Customer(
        cliente_nome="Cliente Premium",
        cliente_email="premium@email.com",
        tipo_solicitacao="Investimento",
        valor_patrimonio=Decimal("200000.00"),
        status="Aguardando Análise",
    )

    db.add(customer)
    db.commit()

    service = WebhookService(db)

    payload = {
        "event_id": "evt_200k",
        "card_id": "card_200k",
        "cliente_email": "premium@email.com",
    }

    result = service.process(payload)

    assert result.prioridade == "prioridade_alta"


def test_should_set_normal_priority_when_patrimonio_is_lower_than_200k(db):
    customer = Customer(
        cliente_nome="Cliente Normal",
        cliente_email="normal@email.com",
        tipo_solicitacao="Investimento",
        valor_patrimonio=Decimal("199999.99"),
        status="Aguardando Análise",
    )

    db.add(customer)
    db.commit()

    service = WebhookService(db)

    payload = {
        "event_id": "evt_normal",
        "card_id": "card_normal",
        "cliente_email": "normal@email.com",
    }

    result = service.process(payload)

    assert result.prioridade == "prioridade_normal"