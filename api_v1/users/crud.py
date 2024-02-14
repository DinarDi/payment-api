from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User
from .schemas import UserCreate
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
    await session.commit()
    await session.refresh(user)
    return user
