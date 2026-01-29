from email.message import EmailMessage

import aiosmtplib
from aiosmtplib import SMTP
from loguru import logger

from core.settings import settings


class EmailClient:
    def __init__(self) -> None:
        self.server: str = settings.SMTP_SERVER
        self.port: int = settings.SMTP_PORT
        self.username: str = settings.SMTP_LOGIN
        self.password: str = settings.SMTP_KEY
        self.from_email: str = settings.SMTP_FROM
        self.from_name: str = settings.SMTP_FROM_NAME

        self._client: SMTP | None = None

    async def connect(self) -> None:
        if self._client and self._client.is_connected:
            return

        self._client = aiosmtplib.SMTP(
            hostname=self.server, port=self.port, start_tls=True, timeout=10
        )

        try:
            await self._client.connect()
            await self._client.login(self.username, self.password)
            logger.info({"event": "smtp", "stage": "connection"})
        except Exception as e:
            self._client = None
            logger.exception({"event": "smtp", "stage": "failure", "error": str(e)})

    async def close(self) -> None:
        if self._client and self._client.is_connected:
            await self._client.quit()
            logger.info({"event": "smtp", "stage": "close"})
        self._client = None

    async def send(
        self,
        to: str,
        subject: str,
        html: str,
        sender_name: str | None = None,
        sender_email: str | None = None,
    ) -> None:
        if self._client is None or not self._client.is_connected:
            await self.connect()

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f'"{sender_name or self.from_name}" <{sender_email or self.from_email}>'
        message["To"] = to

        message.set_content("This email requires an HTML-capable client.")
        message.add_alternative(html, subtype="html")

        try:
            assert self._client is not None, "SMTP client failed to connect"
            await self._client.send_message(message)
        except Exception:
            raise
