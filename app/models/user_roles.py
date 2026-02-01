from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin

if TYPE_CHECKING:
    from .user import DBUser


class UserRole(StrEnum):
    CUSTOMER = "CUSTOMER"
    VENDOR = "VENDOR"
    ADMIN = "ADMIN"
    STAFF = "STAFF"


class DBUserRole(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "user_roles"

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"), nullable=False, default=UserRole.CUSTOMER
    )

    # Foreign Keys
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    vendor_id: Mapped[UUID] = mapped_column(ForeignKey("vendors.id"), nullable=True)

    # Relationship
    user: Mapped["DBUser"] = relationship(back_populates="roles", lazy="selectin")

    def __repr__(self) -> str:
        return f"<UserRole(Role={self.role!r})>"
