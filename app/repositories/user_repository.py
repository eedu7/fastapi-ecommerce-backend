from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBUser
from core.repository import BaseRepository


class UserRepository(BaseRepository[DBUser]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DBUser, session)

    async def get_by_email(self, email: str) -> DBUser | None:
        return await self.get_one_by({"email": email})

    async def get_by_username(self, username: str) -> DBUser | None:
        return await self.get_one_by({"username": username})
