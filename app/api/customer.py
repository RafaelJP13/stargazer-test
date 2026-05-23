from fastapi import APIRouter

router = APIRouter(   
    prefix="/clientes",
    tags=["Clientes"])

@router.post("")
def create_cliente():
    return {
        "message": "endpoint em construção"
    }