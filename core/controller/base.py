from typing import Any, Generic, Mapping, Type, TypeVar
from uuid import UUID

from core.database import Base
from core.exceptions import NotFoundException
from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], repository: BaseRepository) -> None:
        self.model = model
        self.repository = repository

    async def get_by_id(
        self,
        _id: UUID,
    ) -> ModelType:
        db_obj = await self.repository.get_by_id(_id)

        if db_obj is None:
            raise NotFoundException(
                f"{self.model.__tablename__.title()} with id: {_id} does not exists"
            )

        return db_obj

    async def create(self, attributes: Mapping[str, Any]) -> ModelType:
        instance = await self.repository.create(attributes)
        await self._flush()
        return instance

    async def update(self, _id: UUID, attributes: Mapping[str, Any]) -> ModelType:
        db_obj = await self.get_by_id(_id)
        instance = await self.repository.update(db_obj, attributes)
        await self._flush()
        await self._commit()
        return instance  # type: ignore

    async def delete(self, _id: UUID) -> bool:
        db_obj = await self.get_by_id(_id)
        deleted = await self.repository.delete(db_obj)
        await self._commit()
        return deleted

    async def _flush(self) -> None:
        await self.repository.session.flush()

    async def _refresh(self, db_obj: ModelType) -> None:
        await self.repository.session.refresh(db_obj)

    async def _commit(self) -> None:
        await self.repository.session.commit()
