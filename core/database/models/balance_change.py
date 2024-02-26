import enum
from decimal import Decimal
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DECIMAL, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base


class TransactionType(str, enum.Enum):
    WD = 'WITHDRAW'
    DT = 'DEPOSIT'


class BalanceChange(Base):
    account_id: Mapped[int] = mapped_column(
        ForeignKey('account.id'),
    )
    amount: Mapped[Decimal] = mapped_column(
        DECIMAL(10, 2)
    )
    date_time_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc)
    )
    is_accepted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default='False',
    )
    operation_type: Mapped[enum.Enum] = mapped_column(Enum(TransactionType))
