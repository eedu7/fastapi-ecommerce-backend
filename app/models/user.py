from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .user_roles import DBUserRole


class DBUser(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, server_default="false", unique=True
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    roles: Mapped[List["DBUserRole"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )

    __table_args__ = (
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_username", "username", unique=True),
    )

    def __repr__(self) -> str:
        return f"<User(username={self.username!r}, email={self.email!r})>"
