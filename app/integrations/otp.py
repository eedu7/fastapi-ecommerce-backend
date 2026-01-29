import secrets

from app.integrations.redis.client import init_redis


class OTPService:
    def __init__(self) -> None:
        self.prefix = "otp"
        self.ttl = 300
        self.redis = init_redis()

    async def generate(self, email: str) -> None:
        otp = str(secrets.randbelow(1_000_000)).zfill(6)
        await self.redis.set(self._get_key(email), otp, ex=self.ttl)

    async def verify(self, email: str, otp: str) -> bool:
        key = self._get_key(email)
        stored = await self.redis.get(key)

        if not stored or stored != otp:
            return False

        await self.redis.delete(key)
        return True

    def _get_key(self, email: str) -> str:
        return f"{self.prefix}:{email}"
