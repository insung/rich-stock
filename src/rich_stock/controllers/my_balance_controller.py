from fastapi import APIRouter, Depends

from ..controllers.auth_controller import verify_token
from ..models.my_balance_model import (
    MyDomesticBalanceResponse,
)
from ..models.token_credential_model import TokenCredential
from ..repositories.my_balance_repository import (
    KISDomesticBalanceRepository,
    KISOverseasBalanceRepository,
)


my_balance_router = APIRouter(
    prefix="/my_balance", dependencies=[Depends(verify_token)]
)


@my_balance_router.post("/kr", description="국내 주식잔고조회")
async def my_balance(
    token_credential: TokenCredential = Depends(verify_token),
) -> MyDomesticBalanceResponse:
    repository = KISDomesticBalanceRepository(token_credential)
    return await repository.get_my_balance()
