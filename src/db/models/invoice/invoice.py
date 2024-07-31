from __future__ import annotations

from multi_merchant import BaseInvoice
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import TimestampMixin
from ..base.declarative import Base
from ..user import User


class Invoice(Base, BaseInvoice, TimestampMixin):
    __tablename__ = "invoices"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="invoices")
