from decimal import Decimal

from sqlalchemy.orm import Session
from app.services.webhook_service import WebhookService
from app.models.customer import Customer


def test_webhook_priority_high(db: Session):

    customer = Customer(
        cliente_nome="Teste",
        cliente_email="teste@email.com",
        tipo_solicitacao="x",
        valor_patrimonio=Decimal("250000.00"),
        status="Aguardando Análise"
    )

    db.add(customer)
    db.commit()

    service = WebhookService(db)

    payload = {
        "event_id": "evt_1",
        "card_id": "card_1",
        "cliente_email": "teste@email.com"
    }

    result = service.process(payload)

    assert result.status == "Processado"
    assert result.prioridade == "prioridade_alta"


def test_webhook_priority_normal(db: Session):

    customer = Customer(
        cliente_nome="Teste 2",
        cliente_email="normal@email.com",
        tipo_solicitacao="x",
        valor_patrimonio=Decimal("100000.00"),
        status="Aguardando Análise"
    )

    db.add(customer)
    db.commit()

    service = WebhookService(db)

    payload = {
        "event_id": "evt_2",
        "card_id": "card_2",
        "cliente_email": "normal@email.com"
    }

    result = service.process(payload)

    assert result.status == "Processado"
    assert result.prioridade == "prioridade_normal"