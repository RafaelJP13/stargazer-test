from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.schemas.customer import CustomerCreateRequest, CustomerCreateResponse
from app.services.customer_service import CustomerService

router = APIRouter(
    prefix="/clientes"
)

@router.post(
    "",
    response_model=CustomerCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def create_cliente(
    payload: CustomerCreateRequest,
    db: Session = Depends(get_db)
):
    service = CustomerService(db)
    
    try:
        return service.create(payload)

    except IntegrityError as e:
        db.rollback()

        error_msg = str(e.orig).lower()

        if "email" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe um cliente cadastrado com o e-mail '{payload.cliente_email}'.",
            )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um registro com esses dados.",
        )