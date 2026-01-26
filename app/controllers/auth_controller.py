from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import BadRequestException
from core.security import PasswordManager


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(User, user_repository)
        self.user_repository = user_repository

    async def register(self, username: str, email: str, password: str):
        if await self.user_repository.get_by_email(email):
            raise BadRequestException("Email already exists")

        if await self.user_repository.get_by_username(username):
            raise BadRequestException("Username already exists")

        hashed_password = PasswordManager.hash(password)

        user = await self.create(
            {"username": username, "email": email, "password": hashed_password}
        )

        return user
