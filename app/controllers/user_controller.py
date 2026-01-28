from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(User, user_repository)
        self.user_repository = user_repository

    async def get_by_email(self, email: str):
        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise NotFoundException(f"User with email '{email}' not found")

        return user
