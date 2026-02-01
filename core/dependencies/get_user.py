from typing import Annotated

from fastapi import Depends, Request

from app.controllers import UserController
from app.models import DBUser
from core.factory import Factory


async def get_current_user(
    request: Request, controller: Annotated[UserController, Depends(Factory.get_user_controller)]
) -> DBUser:
    user_id = request.state.user.id
    return await controller.get_by_id(user_id)
