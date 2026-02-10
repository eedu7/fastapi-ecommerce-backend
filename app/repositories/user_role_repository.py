from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBUserRole
from core.repository import BaseRepository


class UserRoleRepository(BaseRepository[DBUserRole]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DBUserRole, session)
