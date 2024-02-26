from fastapi import APIRouter

from .auth.views import router as auth_router
from .balance_change.views import router as balance_router

router = APIRouter()
router.include_router(router=auth_router, prefix='/auth')
router.include_router(router=balance_router, prefix='/balance')
