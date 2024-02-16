from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base


if TYPE_CHECKING:
    from .user import User


class Token(Base):
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        unique=True
    )
    refresh_token: Mapped[str | None]

    user: Mapped['User'] = relationship(back_populates='token')
