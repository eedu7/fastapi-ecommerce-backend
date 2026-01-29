from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import AuthController, UserController
from app.repositories import UserRepository
from core.database import get_db


class Factory:
    @staticmethod
    async def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> UserRepository:
        return UserRepository(session)

    @staticmethod
    async def get_auth_controller(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> AuthController:
        return AuthController(user_repository)

    @staticmethod
    async def get_user_controller(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> UserController:
        return UserController(user_repository)
