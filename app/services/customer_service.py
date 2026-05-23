from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.integrations.pipefy import (
    build_create_card_mutation,
    build_update_card_field_mutation,
    build_update_card_field_variables
)
from app.schemas.customer import CustomerCreateRequest

class CustomerService:

    def __init__(self, db):
        self.repository = CustomerRepository(db)

    def create(self, payload: CustomerCreateRequest) -> Customer:

        customer = Customer(
            cliente_nome=payload.cliente_nome,
            cliente_email=payload.cliente_email,
            tipo_solicitacao=payload.tipo_solicitacao,
            valor_patrimonio=payload.valor_patrimonio,
            status="Aguardando Análise"
        )

        saved_customer = self.repository.save(customer)

        mutation = build_create_card_mutation(saved_customer)

        variables = {
            "input": {
                "pipe_id": "PIPE_ID_AQUI",
                "fields_attributes": [
                    {
                        "field_id": "cliente_nome",
                        "field_value": saved_customer.cliente_nome
                    },
                    {
                        "field_id": "cliente_email",
                        "field_value": saved_customer.cliente_email
                    },
                    {
                        "field_id": "valor_patrimonio",
                        "field_value": str(saved_customer.valor_patrimonio)
                    },
                    {
                        "field_id": "tipo_solicitacao",
                        "field_value": saved_customer.tipo_solicitacao
                    },
                ]
            }
        }

        return saved_customer

    def get_by_email(self, email: str) -> Customer | None:
        return self.repository.get_by_email(email)

    def update_status_and_priority(
        self,
        customer: Customer,
        prioridade: str,
        card_id: str
    ) -> Customer:

        customer.status = "Processado"
        customer.prioridade = prioridade

        updated_customer = self.repository.update(customer)

        mutation = build_update_card_field_mutation(
            card_id=card_id,
            field_id="status",
            new_value=customer.status
        )

        variables = build_update_card_field_variables(
            card_id=card_id,
            prioridade=prioridade,
            status=customer.status
        )

        return updated_customer