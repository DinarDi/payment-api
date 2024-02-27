from decimal import Decimal

from pydantic import BaseModel, computed_field

from core.database.models.balance_change import TransactionType


class BalanceChangeBase(BaseModel):
    pass


class BalanceChangeCreate(BalanceChangeBase):
    account_id: int
    amount: Decimal
    operation_type: TransactionType


class PaymentBase(BaseModel):
    pass


class PaymentCreate(PaymentBase):
    value: Decimal
    commission: Decimal
    payment_type: str
    return_url: str

    @computed_field
    def value_with_commission(self) -> Decimal:
        return round(self.value * (1 / (1 - self.commission / 100)), 2)


class PaymentAcceptanceBase(BaseModel):
    pass


class PaymentAcceptanceMetadata(PaymentAcceptanceBase):
    change_id: str
    user_account_id: str


class PaymentAcceptanceIncome(PaymentAcceptanceBase):
    value: str
    currency: str


class PaymentAcceptanceObject(PaymentAcceptanceBase):
    status: str
    metadata: PaymentAcceptanceMetadata
    income_amount: PaymentAcceptanceIncome


class PaymentAcceptanceResponse(PaymentAcceptanceBase):
    type: str
    event: str
    object: PaymentAcceptanceObject
