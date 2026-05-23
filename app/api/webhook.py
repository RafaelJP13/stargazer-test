from fastapi import APIRouter

router = APIRouter(
    prefix="/webhooks/pipefy",
    tags=["Webhooks"]
)

@router.post("/card-updated")
def process_card_updated():
    return {
        "message": "webhook endpoint em construção"
    }