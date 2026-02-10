from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.db.database import get_db
from app.core.redis import init_redis, close_redis
from app.api.v1.verify_endpoint import router as verify_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for initializing Redis connections on application startup
    and closing them on application shutdown.
    """
    # Startup
    print("Starting up...")
    await init_redis()

    yield

    # Shutdown
    print("Shutting down...")
    await close_redis()


app = FastAPI(
    title="KSHRD Certificate Verify Service",
    version="0.0.1",
    description="A FastAPI-based certificate service for verifying KSHRD certificate",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Welcome to Certificate Service API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/db_health_check")
async def check_db(db: AsyncSession = Depends(get_db)):
    """Check database connection health"""
    try:
        result = await db.execute(text("SELECT version();"))
        version = result.scalar()
        return {"status": "online", "database_version": version}
    except Exception as e:
        return {"status": "offline", "error": str(e)}


app.include_router(verify_router, prefix="/api/v1")