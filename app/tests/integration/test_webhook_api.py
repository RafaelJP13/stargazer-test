def test_webhook_returns_message_when_customer_not_found(client):
    response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt-not-found",
            "card_id": "card-1",
            "cliente_email": "naoexiste@email.com",
            "timestamp": "2026-01-01T10:00:00",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "detail": "Evento já processado ou cliente não encontrado"
    }


def test_webhook_duplicate_event_returns_message(client):
    client.post(
        "/clientes",
        json={
            "cliente_nome": "Carlos Silva",
            "cliente_email": "carlos@email.com",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": 150000,
        },
    )

    payload = {
        "event_id": "evt-duplicado",
        "card_id": "card-123",
        "cliente_email": "carlos@email.com",
        "timestamp": "2026-01-01T10:00:00",
    }

    first_response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload,
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/webhooks/pipefy/card-updated",
        json=payload,
    )

    assert second_response.status_code == 200

    assert second_response.json() == {
        "detail": "Evento já processado ou cliente não encontrado"
    }