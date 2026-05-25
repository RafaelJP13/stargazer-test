import os
from app.models.customer import Customer

def build_create_card_mutation() -> str:
    return """
    mutation CreateCard($input: CreateCardInput!) {
        createCard(input: $input) {
            card {
                id
            }
        }
    }
    """.strip()

def build_create_card_variables(customer: Customer) -> dict[str, object]:
    return {
        "input": {
            "pipe_id": os.getenv("PIPE_ID"),
            "fields_attributes": [
                {
                    "field_id": "cliente_nome",
                    "field_value": customer.cliente_nome,
                },
                {
                    "field_id": "cliente_email",
                    "field_value": customer.cliente_email,
                },
                {
                    "field_id": "valor_patrimonio",
                    "field_value": str(customer.valor_patrimonio),
                },
                {
                    "field_id": "tipo_solicitacao",
                    "field_value": customer.tipo_solicitacao,
                },
            ],
        }
    }


def build_update_card_field_mutation() -> str:
    return """
    mutation UpdateCardField($input: UpdateCardFieldInput!) {
        updateCardField(input: $input) {
            success
        }
    }
    """.strip()


def build_update_card_field_variables(
    card_id: str,
    prioridade: str,
    status: str,
) -> list[dict[str, dict[str, str]]]:
    return [
        {
            "input": {
                "card_id": card_id,
                "field_id": "status",
                "new_value": status,
            }
        },
        {
            "input": {
                "card_id": card_id,
                "field_id": "prioridade",
                "new_value": prioridade,
            }
        },
    ]