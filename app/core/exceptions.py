from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.responses import Response
from app.core.constants import ERRO_VALIDACAO
from app.core.serialization import make_json_safe


async def validation_exception_handler(
    request: Request,
    exc: Exception,  # <- AQUI está a correção importante
) -> Response:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "mensagem": ERRO_VALIDACAO,
                "detalhes": make_json_safe(exc.errors()),
            },
        )

    return JSONResponse(
        status_code=500,
        content={"mensagem": "Erro interno"},
    )