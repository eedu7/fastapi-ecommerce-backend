from collections.abc import Mapping, Sequence
from typing import Any, Generic, List, Tuple, Type, TypeVar

from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Load

from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        order_by: List[Tuple[str, str]] | None = None,
        options: List[Load] | None = None,
    ) -> Sequence[ModelType]:
        return await self.get_many_by(
            skip=skip,
            limit=limit,
            order_by=order_by,
            options=options,
        )

    async def get_by_id(
        self,
        id_: Any,
        options: List[Load] | None = None,
    ) -> ModelType | None:
        return await self.session.get(self.model, id_, options=options)

    async def get_one_by(
        self,
        filters: Mapping[str, Any] | None = None,
        options: List[Load] | None = None,
    ) -> ModelType | None:
        stmt = select(self.model)
        stmt = self._apply_options(stmt, options)
        stmt = self._apply_filters(stmt, filters)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many_by(
        self,
        filters: Mapping[str, Any] | None = None,
        order_by: List[Tuple[str, str]] | None = None,
        skip: int = 0,
        limit: int = 20,
        options: List[Load] | None = None,
    ) -> Sequence[ModelType]:
        stmt = select(self.model)

        stmt = self._apply_options(stmt, options)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_order_by(stmt, order_by)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, data: Mapping[str, Any]) -> ModelType:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(
        self,
        instance: ModelType,
        data: Mapping[str, Any],
    ) -> ModelType:
        for field, value in data.items():
            if not hasattr(instance, field):
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute '{field}'"
                )
            setattr(instance, field, value)

        await self.session.flush()
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    def _apply_filters(self, stmt, filters: Mapping[str, Any] | None):
        if not filters:
            return stmt

        for field, value in filters.items():
            column = getattr(self.model, field, None)
            if column is None:
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute '{field}'"
                )

            if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                stmt = stmt.where(column.in_(value))
            else:
                stmt = stmt.where(column == value)

        return stmt

    def _apply_order_by(self, stmt, order_by: List[Tuple[str, str]] | None):
        if not order_by:
            return stmt

        orders = []
        for field, direction in order_by:
            column = getattr(self.model, field, None)
            if column is None:
                raise AttributeError(
                    f"Model {self.model.__name__} has no attribute '{field}'"
                )

            orders.append(desc(column) if direction.lower() == "desc" else asc(column))

        return stmt.order_by(*orders)

    def _apply_options(self, stmt, options: List[Load] | None):
        if not options:
            return stmt
        return stmt.options(*options)
