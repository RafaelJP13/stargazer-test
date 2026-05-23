from app.core.constants import PATRIMONIO_MINIMO_PRIORIDADE_ALTA
from app.repositories.event_repository import EventRepository
from app.services.customer_service import CustomerService
from app.models.event import Event

class WebhookService:

    def __init__(self, db):
        self.event_repository = EventRepository(db)
        self.customer_service = CustomerService(db)

    def process(self, payload: dict):

        event_id = payload["event_id"]

        if self.event_repository.exists(event_id):
            return None

        customer = self.customer_service.get_by_email(
            payload["cliente_email"]
        )

        if not customer:
            return None

        prioridade = (
            "prioridade_alta"
            if customer.valor_patrimonio >= PATRIMONIO_MINIMO_PRIORIDADE_ALTA
            else "prioridade_normal"
        )

        updated_customer = self.customer_service.update_status_and_priority(
            customer=customer,
            prioridade=prioridade,
            card_id=payload["card_id"]
        )

        self.event_repository.save(
            Event(event_id=event_id)
        )

        return updated_customer