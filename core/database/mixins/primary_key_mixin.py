from uuid import uuid4

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, index=True, default=uuid4, sort_order=-10
    )
