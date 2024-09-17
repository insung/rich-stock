from fastapi import APIRouter, Depends

from ..controllers.auth_controller import verify_token
from ..models.my_balance_model import (
    MyBalanceResponse,
)
from ..models.token_credential_model import TokenCredential
from ..repositories.my_balance_repository import (
    KISDomesticBalanceRepository,
    KISOverseasBalanceRepository,
)


my_balance_router = APIRouter(
    prefix="/my_balance", dependencies=[Depends(verify_token)], tags=["My Balance"]
)


@my_balance_router.get("/kr", description="국내 주식잔고조회")
async def get_domestic(
    token_credential: TokenCredential = Depends(verify_token),
) -> MyBalanceResponse:
    repository = KISDomesticBalanceRepository(token_credential)
    return await repository.get_my_balance()


@my_balance_router.get("/overseas", description="해외 주식잔고조회")
async def get_overseas(
    token_credential: TokenCredential = Depends(verify_token),
) -> MyBalanceResponse:
    repository = KISOverseasBalanceRepository(token_credential)
    return await repository.get_my_balance()
