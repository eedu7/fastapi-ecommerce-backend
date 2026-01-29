from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin


class DBUser(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(40), nullable=False, index=True, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User(username={self.username!r}, email={self.email!r})>"
