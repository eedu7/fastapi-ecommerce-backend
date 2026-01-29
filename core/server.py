import os
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from slowapi.middleware import SlowAPIMiddleware

from api import router
from app.integrations.redis.cache import init_cache
from app.integrations.redis.client import close_redis
from core.limiter import init_limiter
from core.middlewares import CorsMiddleware, RequestLoggingMiddleware
from core.settings import settings


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    start_time = time.time()

    logger.info(
        {"event": "server_starting", "pid": os.getpid(), "environment": settings.ENVIRONMENT}
    )

    # Initializing cache
    await init_cache()

    logger.info(
        {
            "event": "server_started",
            "pid": os.getpid(),
            "startup_time_ms": round((time.time() - start_time) * 1000, 2),
        }
    )
    yield
    await close_redis()

    logger.info({"event": "server_stopping", "pid": os.getpid()})


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

    return app
