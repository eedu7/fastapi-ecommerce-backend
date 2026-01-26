from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin


class User(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(40), nullable=False, index=True, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<User(username={self.username!r}, email={self.email!r})>"
