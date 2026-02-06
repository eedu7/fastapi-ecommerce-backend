from typing import Literal

from authlib.integrations.starlette_client import OAuth
from fastapi import Request

from core.settings import settings

oauth = OAuth()

OAuthType = Literal["google", "facebook"]


class SocialAuth:
    def __init__(self) -> None:
        self.oauth = OAuth()
        self.base_redirect_uri = "http://localhost:8000/api/v1/oauth"
        self._register_providers()

    async def login(self, request: Request, provider: OAuthType):
        client = self._get_client(provider)
        redirect_uri = f"{self.base_redirect_uri}/{provider}/callback"
        return await client.authorize_redirect(request, redirect_uri)

    async def callback(self, request: Request, provider: OAuthType):
        client = self._get_client(provider)
        token = await client.authorize_access_token(request)

        match provider:
            case "google":
                user = token
            case "facebook":
                response = await client.get("me?field=id,name,email,picture", token=token)
                user = response.json()

        return {"provider": provider, "user": user}

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
