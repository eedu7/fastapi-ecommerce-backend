from collections.abc import Mapping, Sequence
from typing import Any, Generic, Iterable, List, Tuple, Type, TypeVar

from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load

from core.database import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        order_by: List[Tuple[str, str]] | None = None,
        options: List[Load] | None = None,
    ) -> Sequence[T]:
        return await self.get_by(
            skip=skip, limit=limit, order_by=order_by, options=options
        )

    async def get_by_id(self, _id: Any, options: List[Load] | None = None) -> T | None:
        stmt = select(self.model).where(getattr(self.model, "id") == id)
        stmt = self._apply_options(stmt, options)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, data: Mapping[str, Any]) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.refresh(instance)
        return instance

    async def update(self, _id: Any, data: Mapping[str, Any]) -> T | None:
        instance = await self.get_by_id(_id)
        if instance is None:
            return None

        for field, value in data.items():
            if not hasattr(instance, field):
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute {field}"
                )
            setattr(instance, field, value)

        await self.session.refresh(instance)
        return instance

    async def delete(self, _id: Any) -> bool:
        instance = await self.get_by_id(_id)
        if not instance:
            return False

        await self.session.delete(instance)
        return True

    async def get_by(
        self,
        filters: Mapping[str, Any] | None = None,
        order_by: List[Tuple[str, str]] | None = None,
        skip: int = 0,
        limit: int = 20,
        options: List[Load] | None = None,
    ) -> Sequence[T]:
        stmt = select(self.model)

        stmt = self._apply_options(stmt, options)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_order_by(stmt, order_by)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def _apply_filters(self, stmt, filters: Mapping[str, Any] | None):
        if not filters:
            return stmt

        for field, value in filters.items():
            column = getattr(self.model, field, None)
            if column is None:
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute {field}"
                )
            if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)

        return stmt

    def _apply_order_by(self, stmt, order_by: List[Tuple[str, str]] | None):
        if not order_by:
            return stmt

        for field, direction in order_by:
            column = getattr(self.model, field, None)
            if column is None:
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute {field}"
                )

            if direction.lower() == "desc":
                stmt = stmt.order_by(desc(column))
            else:
                stmt = stmt.order_by(asc(column))
        return stmt

    def _apply_options(self, stmt, options: List[Load] | None):
        if not options:
            return stmt
        return stmt.options(*options)
