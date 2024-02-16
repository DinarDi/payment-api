from enum import Enum

from pydantic import BaseModel


class TokenModeEnum(str, Enum):
    access = 'access_token'
    refresh = 'refresh_token'


class Token(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
