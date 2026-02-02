from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi_cache.decorator import cache

from app.integrations.cache.key_builder import KeyBuilder
from app.models import DBUser
from core.dependencies import authentication_required, get_current_user
from core.limiter import limiter

router = APIRouter()

# TODO: User Routes
# @router.get("/")
# async def get_users(request: Request):
#     pass


# @router.get("/{id}")
# async def get_user(id: UUID, request: Request):
#     pass


# @router.post("/")
# async def create_user(request: Request):
#     pass


# @router.put("/{id}")
# async def update_user(id: UUID, request: Request):
#     pass


# @router.patch("/{id}")
# async def partial_update_user(id: UUID, request: Request):
#     pass


# @router.delete("/{id}")
# async def delete_user(id: UUID, request: Request):
#     pass


# @router.get("/{id}/profile")
# async def get_user_public_profile(id: UUID, request: Request):
#     """
#     response_body: name, avatar, join date, reviews
#     """
#     pass


@router.get("/me", dependencies=[Depends(authentication_required)])
@limiter.limit("10/minute")
@cache(expire=60, key_builder=KeyBuilder.user_me_cache_key)
async def get_user(
    request: Request,
    current_user: Annotated[DBUser, Depends(get_current_user)],
):
    return current_user
