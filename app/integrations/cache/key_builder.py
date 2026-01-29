from typing import Any, Dict, Tuple

from fastapi import Request


class KeyBuilder:
    @staticmethod
    def user_me_cache_key(
        __function: Any,
        __namespace: str = "",
        *,
        request: Request | None = None,
        response: Any = None,
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = {},
    ) -> str:
        """
        Generates a cache key for /me endpoint.
        Only works for authenticated users.
        """
        if request is None:
            raise ValueError("Request is required for user_me_cache_key")

        user = getattr(request.state, "user", None)
        if not user or not getattr(user, "id", None):
            # If user is not authenticated, don't use cache
            raise ValueError("Cannot cache /me for unauthenticated user")

        return f"user:me:{user.id}"
