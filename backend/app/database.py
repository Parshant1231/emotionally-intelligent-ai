# backend/app/database.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./research_data.db")

# Create async engine — async means FastAPI won't block while waiting for DB
engine = create_async_engine(
    DATABASE_URL,
    echo=False,   # Set True to see SQL queries in terminal (useful for debugging)
)

# Session factory — creates DB sessions on demand
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Create all tables on startup if they don't exist."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized")


async def get_db():
    """
    FastAPI dependency — injects a DB session into route handlers.
    Automatically closes session when request is done.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise