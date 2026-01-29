from fastapi import Request

from .keys import CacheKeys


class KeyBuilder:
    @staticmethod
    def user_me_cache_key(func, namespace: str, request: Request, *args, **kwargs) -> str:
        user = request.state.user
        return CacheKeys.user_me(user.id)
