from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Configuration, Payment

from api_v1.auth.views import get_auth_user
from api_v1.balance_change.schemas import BalanceChangeCreate, PaymentCreate
from api_v1.users.schemas import UserWithAccount
from core.config import settings
from core.database import db_settings
from api_v1.balance_change import crud as balance_crud
from core.database.models.balance_change import TransactionType

router = APIRouter(
    tags=['Balance change']
)

Configuration.account_id = settings.ACCOUNT_ID
Configuration.secret_key = settings.SHOP_SECRET_KEY


@router.post('/create_payment')
async def create_payment(
        payload: PaymentCreate,
        session: AsyncSession = Depends(db_settings.create_async_session),
        user: UserWithAccount = Depends(get_auth_user),
):
    change_payload: BalanceChangeCreate = BalanceChangeCreate(
        account_id=user.account.id,
        amount=payload.value,
        operation_type=TransactionType.DT,
    )
    change = await balance_crud.create_change(
        session=session,
        payload=change_payload,
    )

    payment = Payment.create({
        'amount': {
            'value': payload.value_with_commission,
            'currency': 'RUB',
        },
        'payment_method_data': {
            'type': payload.payment_type,
        },
        'confirmation': {
            'type': 'redirect',
            'return_url': payload.return_url,
        },
        'metadata': {
            'table_id': change.id,
            'user_account_id': user.account.id,
        },
        'capture': True,
        'refundable': False,
        'description': 'Пополнение на ' + str(payload.value),
    })

    return JSONResponse(status_code=200, content={
        'confirmation_url': payment.confirmation.confirmation_url,
    })
