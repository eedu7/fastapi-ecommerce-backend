from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger

from core.settings import settings

from .client import init_redis


async def init_cache() -> None:
    try:
        redis = init_redis()
        FastAPICache.init(RedisBackend(redis), prefix=settings.CACHING_PREFIX)
        logger.info(
            {"event": "cache_initialized", "backend": "redis", "prefix": settings.CACHING_PREFIX}
        )
    except Exception as e:
        logger.exception({"event": "cache_init_failed", "error": str(e)})
        raise
