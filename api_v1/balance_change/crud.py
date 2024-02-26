from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import BalanceChange
from .schemas import BalanceChangeCreate


async def create_change(
        session: AsyncSession,
        payload: BalanceChangeCreate,
):
    change: BalanceChange = BalanceChange(
        account_id=payload.account_id,
        amount=payload.amount,
        operation_type=payload.operation_type,
    )
    session.add(change)
    await session.commit()
    await session.refresh(change)
    return change
