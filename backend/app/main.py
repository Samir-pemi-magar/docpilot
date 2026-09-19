from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine
from app.services.storage import storage_service
from app.api.routes.documents import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage_service.ensure_bucket()

    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(documents_router)

@app.get("/health")
async def health_check():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {"status": "ok", "database": "connected"}