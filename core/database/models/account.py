from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .user import User


class Account(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), unique=True)
    balance: Mapped[Decimal]

    user: Mapped['User'] = relationship(back_populates='account')