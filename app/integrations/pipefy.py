def build_create_card_mutation(customer):
    return """
    mutation CreateCard($input: CreateCardInput!) {
        createCard(input: $input) {
            card {
                id
                title
                current_phase {
                    name
                }
            }
        }
    }
    """


def build_update_card_field_mutation(card_id: str, field_id: str, new_value: str):
    return """
    mutation UpdateCardField($input: UpdateCardFieldInput!) {
        updateCardField(input: $input) {
            success
        }
    }
    """


def build_update_card_field_variables(card_id: str, prioridade: str, status: str):
    return [
        {
            "input": {
                "card_id": card_id,
                "field_id": "status",
                "new_value": status
            }
        },
        {
            "input": {
                "card_id": card_id,
                "field_id": "prioridade",
                "new_value": prioridade
            }
        }
    ]