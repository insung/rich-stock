from fastapi import APIRouter, Depends

from ..controllers.auth_controller import verify_token
from ..models.my_balance_model import (
    MyBalanceRequest,
    MyBalanceResponse,
)
from ..models.token_credential_model import TokenCredential
from ..repositories.my_balance_repository import KISMyBalanceRepository


my_balance_router = APIRouter(
    prefix="/my_balance", dependencies=[Depends(verify_token)]
)


@my_balance_router.post("/kr", description="국내 주식잔고조회")
async def my_balance(
    body: MyBalanceRequest, token_credential: TokenCredential = Depends(verify_token)
) -> MyBalanceResponse:
    repository = KISMyBalanceRepository(
        token_credential, token_credential.is_real_domain
    )
    return await repository.get_my_balance()
