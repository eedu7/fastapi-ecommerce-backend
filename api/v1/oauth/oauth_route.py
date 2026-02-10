from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request

from app.controllers import AuthController
from app.integrations.social_auth import OAuthType, SocialAuth
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
    provider: Annotated[OAuthType, Path()],
    oauth: Annotated[SocialAuth, Depends(SocialAuth)],
):
    return await oauth.callback(request=request, provider=provider)
