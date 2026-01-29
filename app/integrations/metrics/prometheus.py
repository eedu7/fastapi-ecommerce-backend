from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_prometheus(app: FastAPI) -> None:
    Instrumentator(
        should_ignore_untemplated=True,
        should_group_status_codes=True,
        should_respect_env_var=True,
        excluded_handlers=["/metrics"],
    ).instrument(app).expose(app, endpoint="/metrics")
