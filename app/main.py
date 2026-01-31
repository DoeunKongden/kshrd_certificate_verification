from sqlalchemy import text
from unittest import result
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from .db.database import get_db

app = FastAPI(
    title="KSHRD Certificate Verify Service",
    version="0.1.0",
    description="A FastAPI-based certificate service for verifying KSHRD certificate",
)


@app.get("/")
async def root():
    return {"message": "Welcome to Certificate Service API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/db_health_checl")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT version();"))
        version = result.scalar()
        return {"status": "online", "database_version": version}
    except Exception as e:
        return {"status": "offline", "error": str(e)}
