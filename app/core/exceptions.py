from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def traduzir_erro(tipo: str, msg: str, ctx: dict | None = None):
    ctx = ctx or {}

    if "value is not a valid email address" in msg:
        return "e-mail inválido"

    if tipo == "value_error.email":
        return "e-mail inválido"

    if "Input should be" in msg and "Atualização Cadastral" in msg:
        return "valor inválido para tipo de solicitação"

    if "Input should be" in msg:
        return "valor inválido para o campo"

    if tipo == "string_too_short":
        return "campo muito curto"

    if tipo == "string_too_long":
        return "campo muito longo"

    if tipo == "missing":
        return "campo obrigatório"

    if tipo == "greater_than_equal":
        return f"valor deve ser maior ou igual a {ctx.get('ge')}"

    return msg  


def validation_exception_handler(request: Request, exc: RequestValidationError):
    erros = []

    for error in exc.errors():
        campo = ".".join(str(x) for x in error.get("loc", []))
        tipo = error.get("type")
        msg_original = error.get("msg")
        ctx = error.get("ctx")

        erros.append({
            "campo": campo,
            "mensagem": traduzir_erro(tipo, msg_original, ctx)
        })

    return JSONResponse(
        status_code=422,
        content={
            "mensagem": "Erro de validação",
            "detalhes": erros
        }
    )