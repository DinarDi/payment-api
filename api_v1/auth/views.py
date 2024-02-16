from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users import crud
from api_v1.users.schemas import UserCreate, UserRead, UserLogin
from . import utils
from .schemas import Token, TokenModeEnum
from core.database.models import User
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


@router.post('/login', response_model=Token)
async def login_user(
        payload: UserLogin,
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password'
    )
    # check user exists
    user: User | None = await crud.get_user_by_username(
        session=session,
        username=payload.username,
    )
    if not user:
        raise error

    # check password match
    if not utils.validate_password(
            password=payload.password,
            hashed_password=user.password,
    ):
        raise error

    # payload for token
    jwt_payload = {
        'sub': user.username,
        'email': user.email
    }
    # create access token
    access_token = utils.encode_jwt(jwt_payload, token_mode=TokenModeEnum.access)
    # create refresh token
    refresh_token = utils.encode_jwt(jwt_payload, token_mode=TokenModeEnum.refresh)
    # save refresh token in database

    return Token(
        token_type='Bearer',
        access_token=access_token,
        refresh_token=refresh_token,
    )
