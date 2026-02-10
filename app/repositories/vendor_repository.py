from sqlalchemy.ext.asyncio import AsyncSession

from app.models import DBVendor
from core.repository import BaseRepository


class VendorRepository(BaseRepository[DBVendor]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(DBVendor, session)
