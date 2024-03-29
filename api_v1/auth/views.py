from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from jwt.exceptions import InvalidTokenError

from api_v1.users import crud as users_crud
from api_v1.auth import crud as auth_crud
from api_v1.users.schemas import UserCreate, UserRead, UserLogin, UserWithAccount
from . import utils
from .schemas import TokenRead, TokenModeEnum, CreateRefreshToken
from core.database.models import User, Token
from core.database import db_settings
from core.redis.redis_settings import RedisTools

router = APIRouter(
    tags=['Auth'],
)

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/refresh_token')


@router.post('/register', response_model=UserRead)
async def create_user(
        payload: UserCreate,
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    return await users_crud.create_user(
        session=session,
        payload=payload
    )


@router.post('/login', response_model=TokenRead)
async def login_user(
        payload: UserLogin,
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password'
    )
    # check user exists
    user: User | None = await users_crud.get_user_by_username(
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
    # save access token in redis
    await RedisTools.set_access_token(
        username=user.username,
        access_token=access_token
    )
    # save refresh token in database
    refresh_token_payload: CreateRefreshToken = CreateRefreshToken(
        user_id=user.id,
        refresh_token=refresh_token,
    )
    await auth_crud.create_refresh_token(
        session=session,
        payload=refresh_token_payload,
    )

    return TokenRead(
        token_type='Bearer',
        access_token=access_token,
        refresh_token=refresh_token,
    )


async def get_new_token(
        token: str = Depends(oauth_scheme),
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'invalid credentials'},
    )
    try:
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token',
        )
    if 'sub' not in payload and 'mode' not in payload:
        raise error
    # check token mode
    if payload['mode'] != TokenModeEnum.refresh:
        raise error
    # get user
    user = await users_crud.get_user_by_username(username=payload['sub'], session=session)
    if not user:
        raise error
    # get refresh token from database
    db_token: Token = await auth_crud.get_token_by_user_id(user_id=user.id, session=session)
    if token != db_token.refresh_token:
        raise error
    # generate new refresh token
    jwt_payload = {
        'sub': user.username,
        'email': user.email,
    }
    new_refresh_token = utils.encode_jwt(
        payload=jwt_payload,
        token_mode=TokenModeEnum.refresh,
    )
    # save new refresh token in database
    setattr(db_token, 'refresh_token', new_refresh_token)
    await session.commit()
    # generate new access token
    new_access_token = utils.encode_jwt(
        payload=jwt_payload,
        token_mode=TokenModeEnum.access,
    )
    # set new access token in redis
    await RedisTools.set_access_token(
        username=user.username,
        access_token=new_access_token,
    )

    return TokenRead(
        token_type='Bearer',
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


@router.post('/refresh_token')
async def refresh_tokens(token: TokenRead = Depends(get_new_token)):
    return token


async def get_auth_user(
        token: str = Depends(oauth_scheme),
        session: AsyncSession = Depends(db_settings.create_async_session),
) -> UserWithAccount:
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={'invalid credentials'},
    )
    try:
        payload = utils.decode_jwt(token=token)
    except InvalidTokenError:
        raise error
    # check token in redis
    token_in_redis = await RedisTools.get_access_token(username=payload['sub'])
    if not token_in_redis or token_in_redis != token:
        raise error
    if 'sub' not in payload and 'mode' not in payload:
        raise error
    # check token mode
    if payload['mode'] != TokenModeEnum.access:
        raise error
    # get user
    user = await users_crud.get_user_with_account(username=payload['sub'], session=session)
    if not user:
        raise error

    return user


@router.get('/users/me', response_model=UserWithAccount)
async def get_user(user: UserWithAccount = Depends(get_auth_user)):
    return user


@router.get('/logout')
async def logout_user(
        user: UserWithAccount = Depends(get_auth_user),
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    # remove refresh token for database
    await auth_crud.delete_refresh_token(
        session=session,
        user_id=user.id,
    )
    # remove access token from redis
    await RedisTools.remove_access_token(username=user.username)
    return {
        'detail': 'logout successful'
    }
