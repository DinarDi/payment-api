from typing import TYPE_CHECKING

from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .account import Account


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    first_name: Mapped[str | None] = mapped_column(String(50))
    last_name: Mapped[str | None] = mapped_column(String(50))
    password: Mapped[bytes] = mapped_column(LargeBinary())

    account: Mapped['Account'] = relationship(back_populates='user')
