from redis import asyncio as aioredis
from redis.asyncio import Redis

from core.settings import settings

_redis: Redis | None = None


def init_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = aioredis.from_url(str(settings.REDIS_URL), encoding="utf-8")
    return _redis


async def close_redis() -> None:
    global _redis

    if _redis:
        await _redis.close()
        await _redis.connection_pool.disconnect()  # type: ignore
        _redis = None
