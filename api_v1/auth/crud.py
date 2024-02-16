from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.schemas import CreateRefreshToken
from core.database.models import Token


async def create_refresh_token(
        session: AsyncSession,
        payload: CreateRefreshToken,
) -> Token:
    # Get exists token
    payload = payload.model_dump(exclude_unset=True)
    stmt = select(Token).where(Token.user_id == payload.get('user_id'))
    result: Result = await session.execute(stmt)
    token = result.scalar_one_or_none()
    # Set new token
    setattr(token, 'refresh_token', payload.get('refresh_token'))
    await session.commit()
    return token
