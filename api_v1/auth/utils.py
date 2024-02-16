from datetime import timedelta, datetime, timezone

import bcrypt
import jwt

from core.config import settings
from .schemas import TokenModeEnum


def hash_password(
        password: str
) -> bytes:
    """
    Function for hash password
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    """
    Function to check password
    :param password: str
    :param hashed_password: bytes
    :return: True | False
    """
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


def encode_jwt(
        payload: dict,
        token_mode: TokenModeEnum,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    """
    Function for encode JWT
    """
    expire_timedelta: timedelta = settings.auth_jwt.access_token_exp \
        if token_mode == TokenModeEnum.access \
        else settings.auth_jwt.refresh_token_exp
    to_encode = payload.copy()
    expire = datetime.now(timezone.utc) + expire_timedelta
    to_encode.update(
        exp=expire,
        mode=token_mode,
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
):
    """
    Function for decode JWT
    """
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded
