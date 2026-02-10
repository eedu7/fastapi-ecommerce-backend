from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import DBUser


class AuthProvider(StrEnum):
    EMAIL = "EMAIL"
    GOOGLE = "GOOGLE"
    FACEBOOK = "FACEBOOK"


class DBUserProvider(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "user_providers"

    provider: Mapped[AuthProvider] = mapped_column(Enum(AuthProvider), name="auth_provider_enum")
    provider_user_id: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="User ID from the OAuth provider"
    )
    provider_email: Mapped[str] = mapped_column(
        String(255), nullable=True, comment="Email from provider (may differ from user.email)"
    )

    # Foreign Keys
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # Relationships
    user: Mapped["DBUser"] = relationship(back_populates="providers")

    __table_args = UniqueConstraint("provider", "provider_user_id", name="uq_provider_user")

    def __repr__(self) -> str:
        return f"<DBUserProvider(user_id={self.user_id}, provider={self.provider})>"
