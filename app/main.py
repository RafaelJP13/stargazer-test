from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.customer import router as customer_router
from app.api.webhook import router as webhook_router
from app.database.connection import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Stargazer Test API",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get(
    "/health",
    tags=["Health"]
)
def health():
    return {
        "status": "ok"
    }


app.include_router(
    customer_router,
    tags=["Clientes"]
)

app.include_router(
    webhook_router,
    tags=["Webhooks"]
)