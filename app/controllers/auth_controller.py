from loguru import logger

from app.models import DBUser
from app.repositories import UserRepository
from app.schemas.extras import Token
from core.controller import BaseController
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTManager, PasswordManager


class AuthController(BaseController[DBUser]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(DBUser, user_repository)
        self.user_repository = user_repository
        self.jwt_manager = JWTManager()

    async def register(self, username: str, email: str, password: str):
        logger.info(
            {
                "event": "user_register",
                "stage": "attempt",
                "username": username,
            }
        )

        if await self.user_repository.get_by_email(email):
            logger.warning(
                {
                    "event": "user_register",
                    "stage": "failed",
                    "reason": "email_exists",
                }
            )
            raise BadRequestException("Email already exists")

        if await self.user_repository.get_by_username(username):
            logger.warning(
                {
                    "event": "user_register",
                    "stage": "failed",
                    "reason": "username_exists",
                }
            )
            raise BadRequestException("Username already exists")

        user = await self.create(
            {
                "username": username,
                "email": email,
                "password": PasswordManager.hash(password),
            }
        )

        logger.info(
            {
                "event": "user_register",
                "stage": "success",
                "user_id": user.id,
            }
        )

        return {"user": user, "token": self._get_token(user)}

    async def login(self, email: str, password: str):
        logger.info(
            {
                "event": "user_login",
                "stage": "attempt",
            }
        )

        user = await self.user_repository.get_by_email(email)

        if user is None or not PasswordManager.verify(password, user.password):
            logger.warning(
                {
                    "event": "user_login",
                    "stage": "failed",
                    "reason": "invalid_credentials",
                }
            )
            raise UnauthorizedException("Invalid email or password")

        logger.info(
            {
                "event": "user_login",
                "stage": "success",
                "user_id": user.id,
            }
        )

        return {"user": user, "token": self._get_token(user)}

    def _get_jti(self, token: str) -> str:
        return self.jwt_manager.decode_ignore_exp(token)["jti"]

    def _get_token(self, user: DBUser) -> Token:
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "username": user.username,
        }

        try:
            access_token = self.jwt_manager.encode(payload, token_type="access")
            refresh_token = self.jwt_manager.encode(payload, token_type="refresh")

            logger.debug(
                {
                    "event": "jwt_generate",
                    "user_id": user.id,
                }
            )
        except Exception:
            logger.exception(
                {
                    "event": "jwt_generate",
                    "stage": "failed",
                    "user_id": user.id,
                }
            )
            raise BadRequestException("Token construction failed")

        return Token(access_token=access_token, refresh_token=refresh_token)
