from loguru import logger

from core.settings import settings


def setup_logging() -> None:
    logger.remove()

    if settings.LOG_TO_FILE:
        settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
        logger.add(
            settings.LOG_DIR / "app.log",
            level=settings.LOG_LEVEL,
            serialize=settings.LOG_JSON,
            rotation=settings.LOG_ROTATION,
            retention=settings.LOG_RETENTION,
            compression=settings.LOG_COMPRESSION if settings.LOG_COMPRESSION else None,
            enqueue=True,
        )
