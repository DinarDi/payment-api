from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Account
from .schemas import AccountDeposit


async def deposit(
        session: AsyncSession,
        payload: AccountDeposit,
):
    stmt = select(Account).where(Account.id == payload.id)
    result: Result = await session.execute(stmt)
    account: Account = result.scalar_one_or_none()
    account.balance += payload.amount

    await session.commit()
    await session.refresh(account)

    return account
