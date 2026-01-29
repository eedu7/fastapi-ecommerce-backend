import secrets

from app.integrations.email import templates
from app.integrations.email.client import EmailClient
from app.integrations.redis.client import init_redis


class EmailService:
    def __init__(self) -> None:
        self.client = EmailClient()
        self.verify_prefix = "verify_email"
        self.verify_ttl = 60 * 60 * 24  # 24 hours
        self.redis = init_redis()

    async def send_otp(self, email: str, otp: str) -> None:
        await self.client.send(to=email, subject="Your OTP Code", html=templates.otp_email(otp))

    async def send_verification(self, email: str) -> None:
        token = await self._create_verification_token(email)
        await self.client.send(
            to=email, subject="Verify your email", html=templates.verify_email(token)
        )

    async def _create_verification_token(self, email: str) -> str:
        token = secrets.token_urlsafe(32)

        await self.redis.set(f"{self.verify_prefix}:{token}", email, ex=self.verify_ttl)
        return token

    async def consume_verification_token(self, token: str) -> str | None:
        key = f"{self.verify_prefix}:{token}"
        email = await self.redis.get(key)
        if not email:
            return None
        await self.redis.delete(key)
        return email
