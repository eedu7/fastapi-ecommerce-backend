from redis import asyncio as aioredis
from redis.asyncio import Redis

from core.settings import settings

redis: Redis | None = None


def init_redis() -> Redis:
    global redis
    if redis is None:
        redis = aioredis.from_url(str(settings.REDIS_URL), encoding="utf-8", decode_response=True)
    return redis


async def close_redis() -> None:
    global redis

    if redis:
        await redis.close()
        redis = None
