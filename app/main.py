from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.events import router as events_router
from app.api.health import router as health_router
from app.database.connection import connect


@asynccontextmanager
async def lifespan(app: FastAPI):
    connect()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(health_router)
app.include_router(events_router)


@app.get("/")
def home():
    return {"message": "Welcome to World Critical"}