from uuid import UUID


class CacheKeys:
    @staticmethod
    def user_me(user_id: str | UUID) -> str:
        return f"user:me:{user_id}"
