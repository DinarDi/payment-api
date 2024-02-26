from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class AccountBase(BaseModel):
    pass


class AccountRead(AccountBase):
    id: int
    balance: Decimal

    model_config = ConfigDict(from_attributes=True)


class AccountDeposit(AccountBase):
    id: int
    amount: Decimal
