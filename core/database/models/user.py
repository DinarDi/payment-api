from typing import Optional

from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    password: Mapped[bytes] = mapped_column(LargeBinary())
