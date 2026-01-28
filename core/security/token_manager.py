from typing import Literal

from core.redis import init_redis


class TokenManager:
    def __init__(self) -> None:
        self.redis = init_redis()

    async def store_token(
        self, jti: str, expires_in: int, token_type: Literal["access", "refresh"] = "access"
    ):
        await self.redis.set(jti, token_type, ex=expires_in)

    async def is_token_blacklisted(self, jti: str) -> bool:
        return await self.redis.exists(jti)

    async def revoke_token(self, jti: str) -> None:
        await self.redis.delete(jti)
