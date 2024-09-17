from fastapi import APIRouter, Depends, Query

from ..models.history_model import DailyHistoryResponse
from ..repositories.history_repository import KISOverseasDailyHistoryRepository
from ..models.token_credential_model import TokenCredential
from ..controllers.auth_controller import verify_token


history_router = APIRouter(
    prefix="/history", dependencies=[Depends(verify_token)], tags=["History"]
)


@history_router.get("/daily")
async def get_daily(
    begin_date: str = Query(description="조회 시작 날짜", examples=["20240901"]),
    end_date: str = Query(description="조회 종료 날짜", examples=["20241001"]),
    token_credential: TokenCredential = Depends(verify_token),
) -> DailyHistoryResponse:
    response = await KISOverseasDailyHistoryRepository(
        token_credential
    ).get_daily_history(begin_date, end_date)
    return response
