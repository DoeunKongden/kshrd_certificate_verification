from curses import echo
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from ..core.config import settings


# 1. The engine: the actual connection "pipe" to PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Logs all the SQL queries to terminal if DEBUG is True
)

# 2. The Session Maker: A factory that creates new "conversations" with the DB
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, 
)


# 3. Base class: for every table that will inherite from
class Base(DeclarativeBase):
    pass


# function for getting database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
