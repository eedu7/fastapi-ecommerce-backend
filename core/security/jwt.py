from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Literal
from uuid import uuid4

from jose import ExpiredSignatureError, JWTError, jwt

from core.exceptions import UnauthorizedException
from core.settings import settings

TokenType = Literal["access", "refresh"]


class JWTDecodeError(UnauthorizedException):
    message = "Invalid token"


class JWTExpiredError(UnauthorizedException):
    message = "Token expired"


class JWTManager:
    def __init__(self) -> None:
        self.secret_key: str = settings.JWT_SECRET
        self.algorithm: str = settings.JWT_ALGORITHM
        self.access_expire_minutes: int = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_expire_minutes: int = settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES
        self.issuer: str | None = getattr(settings, "JWT_ISSUER", None)

    def _get_expire_time(self, token_type: TokenType) -> datetime:
        minutes = (
            self.access_expire_minutes
            if token_type == "access"
            else self.refresh_expire_minutes
        )
        return datetime.now(timezone.utc) + timedelta(minutes=minutes)

    def encode(
        self,
        payload: Dict[str, Any],
        token_type: TokenType = "access",
    ) -> str:
        claims = payload.copy()

        now = datetime.now(timezone.utc)
        expire = self._get_expire_time(token_type)

        claims.update(
            {
                "iat": now,
                "exp": expire,
                "type": token_type,
                "jti": str(uuid4()),
            }
        )

        if self.issuer:
            claims["iss"] = self.issuer

        return jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

    def decode(
        self,
        token: str,
        expected_type: TokenType | None = None,
    ) -> Dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )
        except ExpiredSignatureError:
            raise JWTExpiredError()
        except JWTError:
            raise JWTDecodeError()

        if expected_type and payload.get("type") != expected_type:
            raise JWTDecodeError(message="Invalid token type")

        return payload

    def decode_ignore_exp(self, token: str) -> Dict[str, Any]:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_exp": False},
            )
        except JWTError:
            raise JWTDecodeError()
