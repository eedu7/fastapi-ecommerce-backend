from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        return await self.get_one_by({"email": email})

    async def get_by_username(self, username: str) -> User | None:
        return await self.get_one_by({"username": username})
