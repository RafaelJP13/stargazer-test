from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from app.core.serialization import make_json_safe


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Response:
    return JSONResponse(
        status_code=422,
        content={
            "mensagem": "Erro de validação",
            "detalhes": make_json_safe(exc.errors()),
        },
    )