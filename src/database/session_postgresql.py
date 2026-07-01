from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import settings

pg_user = getattr(settings, 'POSTGRES_USER', 'test_user')
pg_pass = getattr(settings, 'POSTGRES_PASSWORD', 'test_password')
pg_host = getattr(settings, 'POSTGRES_HOST', 'localhost')
pg_port = getattr(settings, 'POSTGRES_DB_PORT', 5432)
pg_db = getattr(settings, 'POSTGRES_DB', 'test_db')

POSTGRESQL_DATABASE_URL = f"postgresql+asyncpg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
postgresql_engine = create_async_engine(POSTGRESQL_DATABASE_URL, echo=False)
AsyncPostgresqlSessionLocal = sessionmaker(  # type: ignore
    bind=postgresql_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

sync_database_url = POSTGRESQL_DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
sync_postgresql_engine = create_engine(sync_database_url, echo=False)


async def get_postgresql_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session.

    This function returns an async generator yielding a new database session.
    It ensures that the session is properly closed after use.

    :return: An asynchronous generator yielding an AsyncSession instance.
    """
    async with AsyncPostgresqlSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_postgresql_db_contextmanager() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an asynchronous database session using a context manager.

    This function allows for managing the database session within a `with` statement.
    It ensures that the session is properly initialized and closed after execution.

    :return: An asynchronous generator yielding an AsyncSession instance.
    """
    async with AsyncPostgresqlSessionLocal() as session:
        yield session
