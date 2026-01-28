from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi.middleware import SlowAPIMiddleware

from api import router
from core.limiter import init_limiter
from core.middlewares import RequestLoggingMiddleware
from core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(str(settings.REDIS_URL))
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


def init_router(app_: FastAPI) -> None:
    app_.include_router(router, prefix="/api")


def make_middleware(app_: FastAPI) -> None:
    app_.add_middleware(SlowAPIMiddleware)
    app_.add_middleware(RequestLoggingMiddleware)


def make_server() -> FastAPI:
    app = FastAPI(title="E-commerce Backend", lifespan=lifespan)
    make_middleware(app)
    init_limiter(app)
    init_router(app)

    return app
