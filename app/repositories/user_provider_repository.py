from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBUserProvider
from core.repository import BaseRepository


class UserProviderRepository(BaseRepository[DBUserProvider]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DBUserProvider, session)
