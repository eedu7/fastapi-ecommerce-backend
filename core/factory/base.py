from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import UserRepository
from core.database import get_db


class Factory:
    @staticmethod
    async def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> UserRepository:
        return UserRepository(session)
