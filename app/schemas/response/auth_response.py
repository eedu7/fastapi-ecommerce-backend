from pydantic import BaseModel, ConfigDict

from app.schemas.extras import Token

from .user_response import UserRead


class AuthRead(BaseModel):
    token: Token
    user: UserRead

    model_config = ConfigDict(from_attributes=True, extra="forbid")
