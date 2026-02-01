from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from api import router
from app.integrations.metrics.prometheus import setup_prometheus
from app.integrations.redis.cache import init_cache
from app.integrations.redis.client import close_redis
from core.limiter import init_limiter
from core.middlewares import CorsMiddleware, RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    # Initializing cache
    await init_cache()

    yield
    await close_redis()


def init_router(app_: FastAPI) -> None:
    app_.include_router(router, prefix="/api")


def make_middleware(app_: FastAPI) -> None:
    app_.add_middleware(CorsMiddleware)
    app_.add_middleware(SlowAPIMiddleware)
    app_.add_middleware(RequestLoggingMiddleware)


def make_server() -> FastAPI:
    app = FastAPI(title="E-commerce Backend", lifespan=lifespan)
    make_middleware(app)
    init_limiter(app)
    init_router(app)
    setup_prometheus(app)

    return app
