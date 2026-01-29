from uuid import UUID

from fastapi_cache import FastAPICache

from .keys import CacheKeys


class UserCache:
    async def invalidate_me(self, user_id: str | UUID) -> None:
        await FastAPICache.clear(key=CacheKeys.user_me(user_id))
