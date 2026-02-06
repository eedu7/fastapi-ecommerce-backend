from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Request

from app.integrations.social_auth import SocialAuth

router = APIRouter()

# oauth = OAuth()

# oauth.register(
#     name="google",
#     client_id=settings.GOOGLE_CLIENT_ID,
#     client_secret=settings.GOOGLE_CLIENT_SECRET,
#     authorize_url="https://accounts.google.com/o/oauth2/auth",
#     authorize_params={"scope": "openid email profile"},
#     access_token_url="https://oauth2.googleapis.com/token",
#     client_kwargs={"scope": "openid email profile"},
#     server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
# )

# oauth.register(
#     name="facebook",
#     client_id=settings.FACEBOOK_APP_ID,
#     client_secret=settings.FACEBOOK_APP_SECRET,
#     authorize_url="https://www.facebook.com/v24.0/dialog/oauth",
#     access_token_url="https://graph.facebook.com/v24.0/oauth/access_token",
#     api_base_url="https://graph.facebook.com/",
#     client_kwargs={"scope": "email public_profile"},
# )


OAuthType = Literal["google", "facebook"]


# TODO: OAuth Routes
# @router.get("/{provider}")
# async def social_provider(request: Request, provider: Annotated[OAuthType, Path()]):
#     if provider == "google":
#         return await oauth.google.authorize_redirect(
#             request, redirect_uri="http://localhost:8000/api/v1/oauth/google/callback"
#         )
#     elif provider == "facebook":
#         redirect_uri = f"http://localhost:8000/api/v1/oauth/{provider}/callback"
#         client = oauth.create_client(provider)
#         return await client.authorize_redirect(request, redirect_uri)


# @router.get("/{provider}/callback")
# async def social_provider_callback(request: Request, provider: Annotated[OAuthType, Path()]):
#     if provider == "google":
#         user = await oauth.google.authorize_access_token(request)
#     elif provider == "facebook":
#         client = oauth.create_client(provider)
#         token = await client.authorize_access_token(request)
#         response = await client.get("me?fields=id,name,email,picture", token=token)
#         user = response.json()

#     return {
#         "provider": provider,
#         "user": user,
#     }


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
