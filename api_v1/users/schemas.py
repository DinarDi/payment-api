from pydantic import BaseModel, EmailStr, ConfigDict

from api_v1.account.schemas import AccountRead


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserWithAccount(UserRead):
    account: AccountRead
    model_config = ConfigDict(from_attributes=True)
