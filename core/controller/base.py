from typing import Any, Generic, Mapping, Type, TypeVar
from uuid import UUID

from core.database import Base
from core.exceptions import NotFoundException
from core.repository import BaseRepository

ModelType = TypeVar("ModelType", bound=Base)


class BaseController(Generic[ModelType]):
    """Base controller providing common CRUD operations for database models."""

    def __init__(self, model: Type[ModelType], repository: BaseRepository) -> None:
        self.model = model
        self.repository = repository

    async def get_by_id(self, _id: UUID) -> ModelType:
        """Retrieve a single record by its ID."""
        db_obj = await self.repository.get_by_id(_id)
        if db_obj is None:
            raise NotFoundException(
                f"{self.model.__tablename__.title()} with id: {_id} does not exists"
            )
        return db_obj

    async def create(self, attributes: Mapping[str, Any]) -> ModelType:
        """Create a new record in the database."""
        instance = await self.repository.create(attributes)
        await self._flush()
        await self._commit()
        return instance

    async def update(self, _id: UUID, attributes: Mapping[str, Any]) -> ModelType:
        """Update an existing record in the database."""
        db_obj = await self.get_by_id(_id)
        instance = await self.repository.update(db_obj, attributes)
        await self._flush()
        await self._commit()
        return instance  # type: ignore

    async def delete(self, _id: UUID) -> bool:
        """Delete a record from the database."""
        db_obj = await self.get_by_id(_id)
        await self.repository.delete(db_obj)
        await self._commit()
        return True

    async def _flush(self) -> None:
        """Send pending changes to database without committing the transaction."""
        await self.repository.session.flush()

    async def _refresh(self, db_obj: ModelType) -> None:
        """Reload object's attributes from the database, discarding unsaved changes."""
        await self.repository.session.refresh(db_obj)

    async def _commit(self) -> None:
        """Commit the current transaction, making all changes permanent."""
        await self.repository.session.commit()
