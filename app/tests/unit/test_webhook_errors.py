from app.services.webhook_service import WebhookService


def test_should_return_none_when_customer_not_found(db):
    service = WebhookService(db)

    payload = {
        "event_id": "evt_not_found",
        "card_id": "card_not_found",
        "cliente_email": "missing@email.com",
    }

    result = service.process(payload)

    assert result is None