from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_settings
from .schemas import PaymentAcceptanceResponse
from api_v1.balance_change import crud as balance_crud
from api_v1.account import crud as account_crud
from ..account.schemas import AccountDeposit


async def acceptance(
        response: PaymentAcceptanceResponse,
        session: AsyncSession = Depends(db_settings.create_async_session),
):
    # Check payment
    if response.event == 'payment.succeeded':
        # If succeeded, update is_accepted and add amount to balance
        await balance_crud.update_change_is_accepted(
            session=session,
            change_id=int(response.object.metadata.change_id),
        )

        account_payload: AccountDeposit = AccountDeposit(
            id=int(response.object.metadata.user_account_id),
            amount=float(response.object.income_amount.value),
        )

        await account_crud.deposit(
            session=session,
            payload=account_payload
        )
    elif response.event == 'payment.canceled':
        # Else delete row from table
        await balance_crud.delete_change(
            session=session,
            change_id=int(response.object.metadata.change_id),
        )
    return True
