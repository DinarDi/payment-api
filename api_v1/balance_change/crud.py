from sqlalchemy import select, Result
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


async def get_change_by_id(
        session: AsyncSession,
        change_id: int,
):
    stmt = select(BalanceChange).where(BalanceChange.id == change_id)
    result: Result = await session.execute(stmt)
    change = result.scalar_one()
    return change


async def update_change_is_accepted(
        session: AsyncSession,
        change_id: int
):
    change: BalanceChange = await get_change_by_id(session=session, change_id=change_id)
    change.is_accepted = True
    await session.commit()
    await session.refresh(change)
    return change


async def delete_change(
        session: AsyncSession,
        change_id: int,
):
    change: BalanceChange = await get_change_by_id(session=session, change_id=change_id)
    await session.delete(change)
