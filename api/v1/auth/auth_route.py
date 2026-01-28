from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.controllers import AuthController
from app.schemas.request.auth_request import AuthLogin, AuthRegister
from app.schemas.response.auth_response import AuthRead
from core.factory import Factory
from core.limiter import limiter

router = APIRouter()


@router.post("/", response_model=AuthRead, status_code=status.HTTP_201_CREATED)
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
