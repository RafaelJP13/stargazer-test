from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field

class CustomerCreateRequest(BaseModel):
    cliente_nome: str = Field(
        ...,
        min_length=3,
        max_length=255
    )
    cliente_email: EmailStr
    tipo_solicitacao: str = Field(
        ...,
        min_length=3,
        max_length=255
    )
    valor_patrimonio: Decimal = Field(
        ...,
        ge=0
    )


class CustomerCreateResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: EmailStr
    status: str