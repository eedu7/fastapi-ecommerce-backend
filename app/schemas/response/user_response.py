from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    id: UUID
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)
