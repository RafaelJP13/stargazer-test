def test_create_customer_invalid_email_returns_422(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "email-invalido",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": 100000,
        },
    )

    assert response.status_code == 422


def test_create_customer_duplicate_email_returns_409(client):
    payload = {
        "cliente_nome": "Maria Silva",
        "cliente_email": "duplicado@email.com",
        "tipo_solicitacao": "Investimento",
        "valor_patrimonio": 50000,
    }

    first_response = client.post(
        "/clientes",
        json=payload,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/clientes",
        json=payload,
    )
    assert second_response.status_code == 409

    body = second_response.json()

    assert "já existe um cliente cadastrado" in body["detail"].lower()
    assert "duplicado@email.com" in body["detail"]


def test_create_customer_missing_cliente_nome_returns_422(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_email": "joao@email.com",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": 100000,
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["mensagem"] == "Erro de validação"


def test_create_customer_negative_patrimonio_returns_422(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao@email.com",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": -100,
        },
    )

    assert response.status_code == 422

    body = response.json()

    assert body["mensagem"] == "Erro de validação"


def test_create_customer_success_returns_201(client):
    response = client.post(
        "/clientes",
        json={
            "cliente_nome": "João Silva",
            "cliente_email": "joao@email.com",
            "tipo_solicitacao": "Investimento",
            "valor_patrimonio": 250000,
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["cliente_nome"] == "João Silva"
    assert body["cliente_email"] == "joao@email.com"
    assert body["status"] == "Aguardando Análise"
    assert "id" in body