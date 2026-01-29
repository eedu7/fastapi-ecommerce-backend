from uuid import UUID

from loguru import logger

from app.models import DBUser
from app.repositories import UserRepository
from core.controller import BaseController
from core.exceptions import NotFoundException


class UserController(BaseController[DBUser]):
    def __init__(self, user_repository: UserRepository) -> None:
        super().__init__(DBUser, user_repository)
        self.user_repository = user_repository

    async def get_by_email(self, email: str):
        logger.info(
            {
                "event": "user_fetch_by_email",
                "stage": "attempt",
            }
        )

        user = await self.user_repository.get_by_email(email)

        if user is None:
            logger.warning(
                {
                    "event": "user_fetch_by_email",
                    "stage": "failed",
                    "reason": "not_found",
                }
            )
            raise NotFoundException("User not found")

        logger.info(
            {
                "event": "user_fetch_by_email",
                "stage": "success",
                "user_id": user.id,
            }
        )

        return user

    async def get_by_id(self, _id: UUID):
        logger.info(
            {
                "event": "user_fetch_by_id",
                "stage": "attempt",
            }
        )

        user = await self.user_repository.get_by_id(_id)

        if user is None:
            logger.warning(
                {
                    "event": "user_fetch_by_id",
                    "stage": "failed",
                    "reason": "not_found",
                }
            )
            raise NotFoundException("User not found")

        logger.info(
            {
                "event": "user_fetch_by_id",
                "stage": "success",
                "user_id": user.id,
            }
        )

        return user
