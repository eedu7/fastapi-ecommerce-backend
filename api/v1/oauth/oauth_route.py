from typing import Annotated, Literal

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Path, Request

from core.settings import settings

router = APIRouter()

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
)

OAuthType = Literal["google", "facebook"]


# TODO: OAuth Routes
@router.get("/{provider}")
async def social_provider(request: Request, provider: Annotated[OAuthType, Path()]):
    return await oauth.google.authorize_redirect(
        request, redirect_uri="http://localhost:8000/api/v1/oauth/google/callback"
    )


@router.get("/{provider}/callback")
async def social_provider_callback(request: Request, provider: Annotated[OAuthType, Path()]):
    token = await oauth.google.authorize_access_token(request)
    return {"token": token}
