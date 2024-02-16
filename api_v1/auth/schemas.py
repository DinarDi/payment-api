from enum import Enum

from pydantic import BaseModel, ConfigDict


class TokenModeEnum(str, Enum):
    access = 'access_token'
    refresh = 'refresh_token'


class TokenBase(BaseModel):
    token_type: str | None = None


class AccessToken(BaseModel):
    access_token: str


class RefreshToken(BaseModel):
    refresh_token: str


class TokenRead(
    TokenBase,
    AccessToken,
    RefreshToken,
):
    model_config = ConfigDict(from_attributes=True)


class CreateRefreshToken(RefreshToken):
    user_id: int
