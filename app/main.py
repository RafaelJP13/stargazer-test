from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models.customer import Customer
from app.models.event import Event


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}