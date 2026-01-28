from app.models import User
from app.repositories import UserRepository
from app.schemas.extras import Token
from core.controller import BaseController
from core.exceptions import BadRequestException, UnauthorizedException
from core.security import JWTManager, PasswordManager


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(User, user_repository)
        self.user_repository = user_repository
        self.jwt_manager = JWTManager()

    async def register(self, username: str, email: str, password: str):
        if await self.user_repository.get_by_email(email):
            raise BadRequestException("Email already exists")

        if await self.user_repository.get_by_username(username):
            raise BadRequestException("Username already exists")

        hashed_password = PasswordManager.hash(password)

        user = await self.create(
            {"username": username, "email": email, "password": hashed_password}
        )

        token = self._get_token(user)

        return {"user": user, "token": token}

    async def login(self, email: str, password: str):
        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise UnauthorizedException("Invalid email or password")

        if not PasswordManager.verify(password, user.password):
            raise UnauthorizedException("Invalid email or password")

        token = self._get_token(user)

        return {"user": user, "token": token}

    def _get_token(self, user: User) -> Token:
        payload = {"sub": str(user.id), "email": user.email, "username": user.username}

        try:
            access_token = self.jwt_manager.encode(payload, token_type="access")
            refresh_token = self.jwt_manager.encode(payload, token_type="refresh")
        except Exception:
            raise BadRequestException("Token construction failed")

        return Token(access_token=access_token, refresh_token=refresh_token)
