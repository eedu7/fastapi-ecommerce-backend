from sys import prefix

from fastapi import APIRouter
from fastapi.routing import APIRoute

from .v1 import v1_router

router = APIRouter()

router.include_router(v1_router, prefix="/v1")
