from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings


class CorsMiddleware(CORSMiddleware):
    def __init__(self, app) -> None:
        allow_origins = [origin for origin in settings.CORS_ORIGINS.split(",")]
        allow_credentials = True

        super().__init__(
            app,
            allow_origins=allow_origins,
            allow_credentials=allow_credentials,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
        )
