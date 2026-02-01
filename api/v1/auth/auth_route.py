from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi_cache.decorator import cache

from app.controllers import AuthController
from app.integrations.cache.key_builder import KeyBuilder
from app.models import DBUser
from app.schemas.request.auth_request import AuthLogin, AuthLogout, AuthRegister
from app.schemas.response.auth_response import AuthRead
from core.dependencies import authentication_required, get_current_user
from core.factory import Factory
from core.limiter import limiter

router = APIRouter()


@router.post("/register", response_model=AuthRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/hour")
async def register(
    request: Request,
    data: AuthRegister,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.register(**data.model_dump())


@router.post("/login", response_model=AuthRead, status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")  # type: ignore
async def login(
    request: Request,
    data: AuthLogin,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.login(**data.model_dump())


@router.post("/logout", dependencies=[Depends(authentication_required)])
@limiter.limit("10/minute")
async def logout(
    request: Request,
    data: AuthLogout,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.logout(**data.model_dump(), user_id=request.state.user.id)


@router.post("/refresh-token")
@limiter.limit("5/minute")
async def refresh_token(request: Request):
    pass


@router.get("/me", dependencies=[Depends(authentication_required)])
@limiter.limit("10/minute")
@cache(expire=60, key_builder=KeyBuilder.user_me_cache_key)
async def get_user(
    request: Request,
    current_user: Annotated[DBUser, Depends(get_current_user)],
):
    return current_user
