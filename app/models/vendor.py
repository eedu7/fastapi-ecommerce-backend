from __future__ import annotations


from core.database import Base
from core.database.mixins import PrimaryKeyMixin, TimestampMixin


class DBVendor(Base, PrimaryKeyMixin, TimestampMixin):
    __tablename__ = "vendors"
