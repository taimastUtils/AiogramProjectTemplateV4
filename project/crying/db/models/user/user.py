from __future__ import annotations
from __future__ import annotations

import datetime
import typing
from enum import StrEnum

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import BaseUser

if typing.TYPE_CHECKING:
    from ..invoice import Invoice


class Locale(StrEnum):
    """Language codes."""
    ENGLISH = 'en'
    RUSSIAN = 'ru'


class User(BaseUser):
    __tablename__ = 'users'
    language_code: Mapped[Locale | None] = mapped_column(default=Locale.RUSSIAN)
    invoices: Mapped[list[Invoice]] = relationship( back_populates='user')

    @classmethod
    async def today_count(cls, session: AsyncSession) -> int:
        result = await session.execute(
            select(cls).where(cls.created_at >= datetime.date.today()))
        return len(result.all())
