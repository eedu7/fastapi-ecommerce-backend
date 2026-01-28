from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from core.settings import settings

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=str(settings.REDIS_URL),
    default_limits=[settings.RATE_LIMIT_DEFAULT],
)


def init_limiter(app_: FastAPI) -> None:
    app_.state.limiter = limiter
    app_.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
