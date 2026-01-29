from uuid import UUID

from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: UUID | None = None
    role: str | None = None
