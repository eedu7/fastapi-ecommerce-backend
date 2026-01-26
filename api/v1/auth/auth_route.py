from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controllers import AuthController
from app.schemas.request.auth_request import AuthLogin, AuthRegister
from app.schemas.response.auth_response import AuthRead
from core.factory import Factory

router = APIRouter()


@router.post("/", response_model=AuthRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: AuthRegister,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.register(**data.model_dump())


@router.post("/login", response_model=AuthRead, status_code=status.HTTP_200_OK)
async def login(
    data: AuthLogin,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.login(**data.model_dump())
