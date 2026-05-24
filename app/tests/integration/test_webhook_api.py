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


def test_webhook_happy_path_processes_customer_successfully(client):
    create_response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao@email.com",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": 250000,
        },
    )

    assert create_response.status_code == 201

    webhook_response = client.post(
        "/webhooks/pipefy/card-updated",
        json={
            "event_id": "evt_123",
            "card_id": "card_456",
            "cliente_email": "joao@email.com",
            "timestamp": "2026-05-18T12:00:00Z",
        },
    )

    assert webhook_response.status_code == 200

    body = webhook_response.json()

    assert body["status"] == "Processado"
    assert body["prioridade"] == "prioridade_alta"
    assert body["message"] == "Card atualizado com sucesso"