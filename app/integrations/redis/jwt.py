from typing import Literal

from core.settings import settings

from .client import init_redis


class TokenStore:
    def __init__(self) -> None:
        self.redis = init_redis()

    async def store_token(self, jti: str, token_type: Literal["access", "refresh"] = "access"):
        if token_type == "access":
            expires_in = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Minutes to seconds
        else:
            expires_in = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES * 60
        await self.redis.set(jti, token_type, ex=expires_in)

    async def is_token_blacklisted(self, jti: str) -> bool:
        return await self.redis.exists(jti)

    async def revoke_token(self, jti: str) -> None:
        await self.redis.delete(jti)
