from fastapi import APIRouter

from .auth import auth_router
from .email import email_router
from .oauth import oauth_router
from .password import password_router
from .token import token_router
from .user import user_router

v1_router = APIRouter()

v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(token_router, prefix="/token", tags=["Token Management"])
v1_router.include_router(password_router, prefix="/auth", tags=["Password Management"])
v1_router.include_router(oauth_router, prefix="/oauth", tags=["OAuth"])
v1_router.include_router(email_router, prefix="/email", tags=["Email"])
v1_router.include_router(user_router, prefix="/users", tags=["User Management"])
