from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from api_v1.users.schemas import UserCreate, UserRead
from core.database import db_settings

router = APIRouter(
    tags=['Auth'],
)


@router.post('/register', response_model=UserRead)
async def create_user(
        payload: UserCreate,
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    return await crud.create_user(
        session=session,
        payload=payload
    )
