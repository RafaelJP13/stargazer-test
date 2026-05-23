from datetime import datetime
from pydantic import BaseModel, EmailStr

class PipefyWebhookRequest(BaseModel):
    event_id: str
    card_id: str
    cliente_email: EmailStr
    timestamp: datetime

class PipefyWebhookResponse(BaseModel):
    message: str
    status: str
    prioridade: str