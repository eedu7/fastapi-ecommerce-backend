from typing import Any, Dict, Literal, TypedDict

from authlib.integrations.starlette_client import OAuth
from fastapi import Request

from core.exceptions import BadRequestException, UnauthorizedException
from core.settings import settings

OAuthType = Literal["google", "facebook"]


class ProviderUser(TypedDict):
    provider_id: str
    full_name: str
    first_name: str
    last_name: str
    email: str
    picture_url: str


class SocialAuth:
    def __init__(self) -> None:
        self.oauth = OAuth()
        self.base_redirect_uri = "http://localhost:8000/api/v1/oauth"
        self._register_providers()

    async def login(self, request: Request, provider: OAuthType):
        client = self._get_client(provider)
        redirect_uri = f"{self.base_redirect_uri}/{provider}/callback"
        return await client.authorize_redirect(request, redirect_uri)

    async def callback(self, request: Request, provider: OAuthType) -> ProviderUser:
        client = self._get_client(provider)
        token = await client.authorize_access_token(request)

        if not token:
            raise UnauthorizedException("OAuth token exchange failed")

        match provider:
            case "google":
                if "userinfo" not in token:
                    raise BadRequestException("Google userinfo missing")

                user_data = token.get("userinfo", None)
                return self._normalize_user("google", user_data)

            case "facebook":
                response = await client.get(
                    "me",
                    params={
                        "fields": "id,name,email,first_name,last_name,picture.width(500).height(500)"
                    },
                    token=token,
                )
                fb_user_data = response.json()

                if "error" in fb_user_data:
                    raise BadRequestException("Facebook API error")

                return self._normalize_user("facebook", fb_user_data)

    def _register_providers(self) -> None:
        self._register_google()
        self._register_facebook()

    def _register_google(self) -> None:
        self.oauth.register(
            name="google",
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            authorize_url="https://accounts.google.com/o/oauth2/auth",
            authorize_params={"scope": "openid email profile"},
            access_token_url="https://oauth2.googleapis.com/token",
            client_kwargs={"scope": "openid email profile"},
            server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        )

    def _register_facebook(self) -> None:
        self.oauth.register(
            name="facebook",
            client_id=settings.FACEBOOK_APP_ID,
            client_secret=settings.FACEBOOK_APP_SECRET,
            authorize_url="https://www.facebook.com/v24.0/dialog/oauth",
            access_token_url="https://graph.facebook.com/v24.0/oauth/access_token",
            api_base_url="https://graph.facebook.com/",
            client_kwargs={"scope": "email public_profile"},
        )

    def _get_client(self, provider: OAuthType):
        client = self.oauth.create_client(provider)
        if not client:
            raise ValueError("Unsupported OAuth provider")
        return client

    def _normalize_user(self, provider: OAuthType, user_info: Dict[str, Any]) -> ProviderUser:
        match provider:
            case "google":
                return self._normalize_google_user(user_info)
            case "facebook":
                return self._normalize_facebook_user(user_info)
            case _:
                raise ValueError(f"Unsupported provider: {provider}")

    def _normalize_google_user(self, user_info: Dict[str, Any]) -> ProviderUser:
        return {
            "provider_id": user_info["sub"],
            "full_name": user_info["name"],
            "first_name": user_info["given_name"],
            "last_name": user_info["family_name"],
            "email": user_info["email"],
            "picture_url": user_info["picture"],
        }

    def _normalize_facebook_user(self, user_info: Dict[str, Any]) -> ProviderUser:
        return {
            "provider_id": user_info["id"],
            "full_name": user_info["name"],
            "email": user_info["email"],
            "picture_url": user_info["picture"]["data"]["url"],
            "first_name": user_info["first_name"],
            "last_name": user_info["last_name"],
        }
