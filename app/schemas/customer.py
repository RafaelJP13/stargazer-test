from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class TipoSolicitacao(str, Enum):
    atualizacao_cadastral = "Atualização Cadastral"

class CustomerCreateRequest(BaseModel):
    cliente_nome: str = Field(
        ...,
        min_length=3,
        max_length=255,
        description="Nome do cliente"
    )

    cliente_email: EmailStr = Field(
        ...,
        description="E-mail do cliente"
    )

    tipo_solicitacao: TipoSolicitacao = Field(
        ...,
        description="Tipo da solicitação permitida"
    )

    valor_patrimonio: Decimal = Field(
        ...,
        ge=0,
        decimal_places=2,
        description="Valor do patrimônio (não pode ser negativo)"
    )

class CustomerCreateResponse(BaseModel):
    id: int
    cliente_nome: str
    cliente_email: EmailStr
    status: str