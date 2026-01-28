from fastapi import APIRouter

from .auth import auth_router
from .user import user_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(user_router, prefix="/users", tags=["User Management"])
