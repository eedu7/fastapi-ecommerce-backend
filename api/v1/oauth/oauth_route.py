from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request

from app.integrations.social_auth import OAuthType, SocialAuth

router = APIRouter()


@router.get("/{provider}")
async def social_login(
    request: Request,
    provider: Annotated[OAuthType, Path()],
    oauth: Annotated[SocialAuth, Depends(SocialAuth)],
):
    return await oauth.login(request=request, provider=provider)


@router.get("/{provider}/callback")
async def social_login_callback(
    request: Request,
    provider: Annotated[OAuthType, Path()],
    oauth: Annotated[SocialAuth, Depends(SocialAuth)],
):
    return await oauth.callback(request=request, provider=provider)
