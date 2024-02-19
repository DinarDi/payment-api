from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.database.models import User, Account, Token
from .schemas import UserCreate, UserWithAccount
from ..auth.utils import hash_password


async def create_user(
        session: AsyncSession,
        payload: UserCreate,
) -> User:
    user_in = payload.model_dump()
    user_password = hash_password(user_in.get('password'))
    user: User = User(
        username=user_in.get('username'),
        email=user_in.get('email'),
        first_name=user_in.get('first_name'),
        last_name=user_in.get('last_name'),
        password=user_password,
    )
    session.add(user)
    await session.flush()

    # Create account for user
    account = Account(user_id=user.id)
    session.add(account)
    # Create token for user
    token = Token(user_id=user.id)
    session.add(token)

    await session.commit()
    await session.refresh(user)

    return user


async def get_user_by_username(
        session: AsyncSession,
        username: str,
) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar_one_or_none()
    return user


async def get_user_with_account(
        session: AsyncSession,
        username: str,
):
    stmt = select(User).where(User.username == username).options(joinedload(User.account))
    result: Result = await session.execute(stmt)
    user: UserWithAccount = result.scalar_one_or_none()
    return user
