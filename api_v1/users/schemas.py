from pydantic import BaseModel, EmailStr, ConfigDict


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
