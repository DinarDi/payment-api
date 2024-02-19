from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.schemas import CreateRefreshToken
from core.database.models import Token


async def get_token_by_user_id(
        session: AsyncSession,
        user_id: int,
) -> Token:
    stmt = select(Token).where(Token.user_id == user_id)
    result: Result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    return token


async def create_refresh_token(
        session: AsyncSession,
        payload: CreateRefreshToken,
) -> Token:
    # Get exists token
    payload = payload.model_dump()
    stmt = select(Token).where(Token.user_id == payload.get('user_id'))
    result: Result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    # Set new token
    setattr(token, 'refresh_token', payload.get('refresh_token'))
    await session.commit()
    return token
