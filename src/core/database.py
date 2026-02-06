"""Database connection and session management."""

import ssl
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.core.config import get_settings

settings = get_settings()

# Configure SSL for Neon PostgreSQL
connect_args = {}
if settings.requires_ssl:
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    connect_args["ssl"] = ssl_context

engine = create_async_engine(
    settings.async_database_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,
    connect_args=connect_args,
)

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_tables() -> None:
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables() -> None:
    """Drop all database tables (for testing)."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
