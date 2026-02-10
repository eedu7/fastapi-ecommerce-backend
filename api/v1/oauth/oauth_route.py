from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request, Response

from app.controllers import AuthController
from app.integrations.social_auth import OAuthType
from core.factory import Factory

router = APIRouter()


@router.get("/{provider}")
async def social_login(
    request: Request,
    provider: Annotated[OAuthType, Path()],
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.social_login(request=request, provider=provider)


@router.get("/{provider}/callback")
async def social_login_callback(
    request: Request,
    response: Response,
    provider: Annotated[OAuthType, Path()],
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.social_login_callback(
        request=request, response=response, provider=provider
    )
