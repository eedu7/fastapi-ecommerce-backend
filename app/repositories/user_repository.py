from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)
