from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import aiohttp
from fastapi import HTTPException, status

from ..models.history_model import DailyHistoryDetailResponse, DailyHistoryResponse
from ..entities.kis_history_entity import (
    KISDomesticDailyHistoryRequest,
    KISDomesticDailyHistoryResponse,
    KISOverseasDailyHistoryRequest,
    KISOverseasDailyHistoryResponse,
)
from ..entities.kis_base_entity import KISRequestHeaderBase
from ..models.token_credential_model import TokenCredential


class DailyHistoryRepository(ABC):
    @abstractmethod
    async def get_daily_history(
        self, begin_date: str, end_date: str
    ) -> DailyHistoryResponse:
        raise NotImplementedError


class KISDomesticDailyHistoryRepository(DailyHistoryRepository):
    def __init__(self, token_credential: TokenCredential):
        # [참고] 3개월 이전의 체결은 tr_id 가 다르다. (실전: CTSC9115R / 모의: VTSC9115R)
        tr_id = "TTTC8001R" if token_credential.is_real_domain else "VTTC8001R"
        self.token_credential = token_credential
        self.url = (
            token_credential.get_domain_url()
            + "/uapi/domestic-stock/v1/trading/inquire-daily-ccld"
        )
        self.kis_request_header = KISRequestHeaderBase(
            authorization=f"{token_credential.token_type} {token_credential.access_token}",
            appkey=token_credential.appkey,
            appsecret=token_credential.appsecret,
            tr_id=tr_id,
        ).model_dump()

    async def get_daily_history(
        self, begin_date: str, end_date: str
    ) -> DailyHistoryResponse:

        if datetime.strptime(begin_date, "%Y%m%d") < (
            datetime.today() - timedelta(days=90)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="3개월 이전의 데이터는 조회할 수 없습니다.",
            )

        kis_request_body = KISDomesticDailyHistoryRequest(
            account_number=self.token_credential.get_account_number_prefix(),
            account_code=self.token_credential.get_account_number_suffix(),
            begin_date=begin_date,
            end_date=end_date,
        ).model_dump(by_alias=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params=kis_request_body,
                headers=self.kis_request_header,
            ) as response:
                text = await response.text()

            kis_response = KISDomesticDailyHistoryResponse.model_validate_json(text)

            if kis_response.isSuccess() is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="국내 일별 거래내역 조회 실패",
                )

            return DailyHistoryResponse(
                items=[
                    DailyHistoryDetailResponse(
                        trade_day=item.ord_dt,
                        sell_buy_type=item.sll_buy_dvsn_cd,
                        ticker=item.pdno,
                        ticker_name=item.prdt_name,
                        trade_quantity=item.tot_ccld_qty,
                        trade_quantity_decimal=0.0,
                        trade_price_unit=item.ord_unpr,
                        trade_price=item.tot_ccld_amt,
                        trade_fee=0.0,
                        currency="KRW",
                    )
                    for item in kis_response.output1
                ],
                total_buy_amount=kis_response.output2.tot_ccld_amt,
                total_sell_amount=0.0,
            )


class KISOverseasDailyHistoryRepository(DailyHistoryRepository):
    def __init__(self, token_credential: TokenCredential):
        tr_id = "CTOS4001R"
        self.token_credential = token_credential
        self.url = (
            token_credential.get_domain_url()
            + "/uapi/overseas-stock/v1/trading/inquire-period-trans"
        )
        self.kis_request_header = KISRequestHeaderBase(
            authorization=f"{token_credential.token_type} {token_credential.access_token}",
            appkey=token_credential.appkey,
            appsecret=token_credential.appsecret,
            tr_id=tr_id,
        ).model_dump()

    async def get_daily_history(
        self, begin_date: str, end_date: str
    ) -> DailyHistoryResponse:
        kis_request_body = KISOverseasDailyHistoryRequest(
            account_number=self.token_credential.get_account_number_prefix(),
            account_code=self.token_credential.get_account_number_suffix(),
            begin_date=begin_date,
            end_date=end_date,
        ).model_dump(by_alias=True)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params=kis_request_body,
                headers=self.kis_request_header,
            ) as response:
                text = await response.text()

            kis_response = KISOverseasDailyHistoryResponse.model_validate_json(text)

            if kis_response.isSuccess() is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="해외 일별 거래내역 조회 실패",
                )

            return DailyHistoryResponse(
                items=[
                    DailyHistoryDetailResponse(
                        trade_day=item.trad_dt,
                        sell_buy_type=item.sll_buy_dvsn_cd,
                        ticker=item.pdno,
                        ticker_name=item.ovrs_item_name,
                        trade_quantity=item.ccld_qty,
                        trade_quantity_decimal=item.amt_unit_ccld_qty,
                        trade_price_unit=item.ft_ccld_unpr2,
                        trade_price=item.tr_frcr_amt2,
                        trade_fee=item.frcr_fee1,
                        currency=item.crcy_cd,
                    )
                    for item in kis_response.output1
                ],
                total_buy_amount=kis_response.output2.frcr_buy_amt_smtl,
                total_sell_amount=kis_response.output2.frcr_sll_amt_smtl,
            )
