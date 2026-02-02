from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.controllers import AuthController
from app.schemas.extras import Token
from app.schemas.request.token_request import RefreshTokenRequest
from core.factory import Factory
from core.limiter import limiter

router = APIRouter()


@router.post("/refresh", response_model=Token)
@limiter.limit("5/minute")
async def refresh_token(
    request: Request,
    data: RefreshTokenRequest,
    controller: Annotated[AuthController, Depends(Factory.get_auth_controller)],
):
    return await controller.refresh_token(data.refresh_token)
