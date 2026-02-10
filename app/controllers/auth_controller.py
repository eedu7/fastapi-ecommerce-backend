from uuid import UUID

from fastapi import Request, Response

from app.integrations import SocialAuth
from app.integrations.cache.user_cache import UserCache
from app.integrations.jwt_token_store import JWTTokenStore
from app.integrations.social_auth import OAuthType
from app.models import DBUser
from app.repositories import UserRepository
from app.schemas.extras import Token
from core.controller import BaseController
from core.exceptions import BadRequestException, NotFoundException, UnauthorizedException
from core.security import JWTManager, PasswordManager


class AuthController(BaseController[DBUser]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(DBUser, user_repository)
        self.user_repository = user_repository
        self.jwt_manager = JWTManager()
        self.jwt_token_store = JWTTokenStore()
        self.social_auth = SocialAuth()

    async def register(self, username: str, email: str, password: str, response: Response):
        if await self.user_repository.get_by_email(email):
            raise BadRequestException("Email already exists")

        if await self.user_repository.get_by_username(username):
            raise BadRequestException("Username already exists")

        user = await self.create(
            {
                "username": username,
                "email": email,
                "password": PasswordManager.hash(password),
            }
        )
        token = self._get_token(user)
        self._set_cookies(response, token)

        return {"user": user, "token": token}

    async def login(self, email: str, password: str, response: Response):
        user = await self.user_repository.get_by_email(email)

        if user is None or not PasswordManager.verify(password, user.password):
            raise UnauthorizedException("Invalid email or password")

        token = self._get_token(user)
        self._set_cookies(response, token)

        return {"user": user, "token": token}

    async def social_login(self, request: Request, provider: OAuthType) -> None:
        return await self.social_auth.login(request, provider)

    async def logout(
        self, user_id: UUID, access_token: str, refresh_token: str, response: Response
    ):
        try:
            access_jti = self.jwt_manager.get_jti(access_token)
            refresh_jti = self.jwt_manager.get_jti(refresh_token)

            await UserCache.invalidate_me(user_id)

            await self.jwt_token_store.store_token(access_jti)
            await self.jwt_token_store.store_token(refresh_jti)

            self._delete_cookies(response)

        except Exception:
            raise BadRequestException("Logout failed")

    async def refresh_token(self, refresh_token: str, response: Response):
        jti = self.jwt_manager.get_jti(refresh_token)
        blacklisted = await self.jwt_token_store.is_token_blacklisted(jti)

        if blacklisted:
            raise BadRequestException("Invalid token")

        payload = self.jwt_manager.decode_ignore_exp(refresh_token)
        user_id = payload.get("sub", None)

        if user_id is None:
            raise NotFoundException("User not found")

        user = await self.get_by_id(user_id)

        await self.jwt_token_store.store_token(jti, "refresh")

        token = self._get_token(user)

        self._set_cookies(response, token)

        return token

    def _get_token(self, user: DBUser) -> Token:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
        }

        try:
            access_token = self.jwt_manager.encode(payload, token_type="access")
            refresh_token = self.jwt_manager.encode(payload, token_type="refresh")

        except Exception:
            raise BadRequestException("Token construction failed")

        return Token(access_token=access_token, refresh_token=refresh_token)

    def _set_cookies(self, response: Response, token: Token) -> None:
        response.set_cookie(key="accessToken", value=token.access_token)
        response.set_cookie(key="refreshToken", value=token.refresh_token)

    def _delete_cookies(self, response: Response) -> None:
        response.delete_cookie("accessToken")
        response.delete_cookie("refreshToken")
