from decimal import Decimal
from app.services.webhook_service import WebhookService
from app.models.customer import Customer


def test_event_idempotency(db):

    customer = Customer(
        cliente_nome="Teste",
        cliente_email="dup@email.com",
        tipo_solicitacao="x",
        valor_patrimonio=Decimal("250000.00"),
        status="Aguardando Análise"
    )

    db.add(customer)
    db.commit()

    service = WebhookService(db)

    payload = {
        "event_id": "evt_duplicate",
        "card_id": "card_1",
        "cliente_email": "dup@email.com"
    }

    result1 = service.process(payload)
    result2 = service.process(payload)

    assert result1 is not None
    assert result1.status == "Processado"

    assert result2 is None