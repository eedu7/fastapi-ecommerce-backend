from typing import List

from fastapi import FastAPI
from fastapi.middleware import Middleware

from api import router


def init_router(app_: FastAPI) -> None:
    app_.include_router(router, prefix="/api")


def make_middleware() -> List[Middleware]:
    return []


def make_server() -> FastAPI:
    app = FastAPI(title="ECommerce Backend", middleware=make_middleware())

    init_router(app)

    return app
