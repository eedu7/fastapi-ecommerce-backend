from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware

from api import router
from core.limiter import init_limiter


def init_router(app_: FastAPI) -> None:
    app_.include_router(router, prefix="/api")


def make_middleware(app_: FastAPI) -> None:
    app_.add_middleware(SlowAPIMiddleware)


def make_server() -> FastAPI:
    app = FastAPI(
        title="E-commerce Backend",
    )
    make_middleware(app)
    init_limiter(app)
    init_router(app)

    return app
