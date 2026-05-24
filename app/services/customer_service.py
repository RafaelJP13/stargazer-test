from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.integrations.pipefy import (
    build_create_card_mutation,
    build_create_card_variables,
    build_update_card_field_mutation,
    build_update_card_field_variables,
)
from app.schemas.customer import CustomerCreateRequest
class CustomerService:

    def __init__(self, db: object) -> None:
        self.repository = CustomerRepository(db)

    def create(self, payload: CustomerCreateRequest) -> Customer:

        customer = Customer(
            cliente_nome=payload.cliente_nome,
            cliente_email=payload.cliente_email,
            tipo_solicitacao=payload.tipo_solicitacao,
            valor_patrimonio=payload.valor_patrimonio,
            status="Aguardando Análise",
        )

        saved_customer = self.repository.save(customer)

        mutation:  str                  = build_create_card_mutation()
        variables: dict[str, object]    = build_create_card_variables(saved_customer)

        return saved_customer

    def get_by_email(self, email: str) -> Customer | None:
        return self.repository.get_by_email(email)

    def update_status_and_priority(
        self,
        customer: Customer,
        prioridade: str,
        card_id: str,
    ) -> Customer:

        customer.status = "Processado"
        customer.prioridade = prioridade

        updated_customer = self.repository.update(customer)

        mutation:  str                              = build_update_card_field_mutation()
        variables: list[dict[str, dict[str, str]]] = build_update_card_field_variables(
            card_id=card_id,
            prioridade=prioridade,
            status=customer.status,
        )

        return updated_customer