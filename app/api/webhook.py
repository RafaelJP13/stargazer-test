from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.webhook import PipefyWebhookRequest, PipefyWebhookResponse
from app.services.webhook_service import WebhookService

router = APIRouter(
    prefix="/webhooks/pipefy"
)

@router.post(
    "/card-updated",
    response_model=PipefyWebhookResponse
)
def process_card_updated(
    payload: PipefyWebhookRequest,
    db: Session = Depends(get_db)
):
    service = WebhookService(db)
    result = service.process(payload.model_dump())

    if result is None:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Evento já processado ou cliente não encontrado"}
        )

    return PipefyWebhookResponse(
        message="Card atualizado com sucesso",
        status=result.status,
        prioridade=result.prioridade
    )