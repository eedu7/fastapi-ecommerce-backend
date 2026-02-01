from uuid import UUID


from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class UserController(BaseController[DBUser]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(DBUser, user_repository)
        self.user_repository = user_repository

    async def get_by_email(self, email: str):
        user = await self.user_repository.get_by_email(email)

        if user is None:
            raise NotFoundException("User not found")

        return user

    async def get_by_id(self, _id: UUID):
        user = await self.user_repository.get_by_id(_id)

        if user is None:
            raise NotFoundException("User not found")

        return user
