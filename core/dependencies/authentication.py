from typing import Annotated
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.extras import CurrentUser
from core.exceptions import UnauthorizedException
from core.security import JWTManager


class AuthenticationRequired:
    def __init__(
        self,
        request: Request,
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))],
    ) -> None:
        if not token:
            raise UnauthorizedException("Token is missing.")

        try:
            payload = JWTManager().decode(token.credentials)

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
