from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health")
async def health_check():
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))

    return {"status": "ok", "database": "connected"}