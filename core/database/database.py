from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from core.settings import settings

logger.info(
    {
        "event": "db_engine_init",
        "driver": "postgresql+asyncpg",
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_recycle": settings.DB_POOL_RECYCLE,
    }
)


async_engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DB_ECHO,
    pool_pre_ping=settings.DB_POOL_PRE_PING,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug(
        {
            "event": "db_session",
            "stage": "open",
        }
    )

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            logger.warning(
                {
                    "event": "db_session",
                    "stage": "rollback",
                }
            )
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.debug(
                {
                    "event": "db_session",
                    "stage": "close",
                }
            )


async def dispose_db_engine() -> None:
    logger.info(
        {
            "event": "db_engine",
            "stage": "disposing",
        }
    )

    await async_engine.dispose()

    logger.info(
        {
            "event": "db_engine",
            "stage": "disposed",
        }
    )
