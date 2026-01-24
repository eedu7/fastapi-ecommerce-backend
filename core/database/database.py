from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import settings

async_engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DB_ECHO,  # Set "True" for SQL Logging
    pool_pre_ping=settings.DB_POOL_PRE_PING,  # Verify connections before use
    pool_size=settings.DB_POOL_SIZE,  # Max connections in pool
    max_overflow=settings.DB_MAX_OVERFLOW,  # Extra connections when pool full
    pool_recycle=settings.DB_POOL_RECYCLE,  # Recycle connections after 1 hour
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,  # Explicit control over flushing
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def dispose_db_engine() -> None:
    """Dispose database engine on application shutdown"""
    await async_engine.dispose()
