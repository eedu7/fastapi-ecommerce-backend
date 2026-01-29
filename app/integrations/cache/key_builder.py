from typing import Any, Dict, Tuple

from fastapi import Request

from .keys import CacheKeys


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
        if request is None:
            raise ValueError("Request is required for user_me_cache_key")
        user = request.state.user
        return CacheKeys.user_me(user.id)
