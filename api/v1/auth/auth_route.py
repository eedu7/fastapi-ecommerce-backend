from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.controllers import AuthController
from app.schemas.request.auth_request import AuthLogin, AuthRegister
from app.schemas.response.auth_response import AuthRead
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


@router.post("/logout")
async def logout(request: Request):
    pass


@router.post("/refresh-token")
async def refresh_token(request: Request):
    pass


@router.post("/forgot-password")
async def forgot_password(request: Request):
    pass


@router.post("/reset-password")
async def reset_password(request: Request):
    pass


@router.post("/verify-email")
async def verify_email(request: Request):
    pass


@router.post("/resend-verification")
async def resend_verification(request: Request):
    pass


@router.post("/change-password")
async def change_password(request: Request):
    pass


@router.get("/me")
async def get_user(request: Request):
    pass
