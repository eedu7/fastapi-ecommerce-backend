from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.integrations.jwt_token_store import JWTTokenStore
from app.schemas.extras import CurrentUser
from core.exceptions import UnauthorizedException
from core.security import JWTManager


async def authentication_required(
    request: Request,
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))],
    jwt_manager: Annotated[JWTManager, Depends(JWTManager)],
    jwt_token_store: Annotated[JWTTokenStore, Depends(JWTTokenStore)],
):
    if not token:
        raise UnauthorizedException("Token is missing.")

    payload = jwt_manager.decode(token.credentials)

    blacklisted = await jwt_token_store.is_token_blacklisted(str(payload.get("jti")))

    if blacklisted:
        raise UnauthorizedException("Invalid token")

    try:
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid token")
        user_id = UUID(user_id)
        role = payload.get("role")

        if not hasattr(request.state, "user"):
            request.state.user = CurrentUser()

        request.state.user.id = user_id
        request.state.user.role = role
    except Exception:
        raise UnauthorizedException("Invalid or expired token")
