from abc import ABC, abstractmethod

import aiohttp
from fastapi import HTTPException, status

from ..entities.kis_base_entity import KISRequestHeaderBase
from ..entities.kis_balance_entity import (
    KISDomesticBalanceRequest,
    KISDomesticBalanceResponse,
    KISOverseasBalanceRequest,
    KISOverseasBalanceResponse,
)
from ..models.my_balance_model import MyDomesticBalanceResponse
from ..models.token_credential_model import TokenCredential


class MyBalanceRepositoryABC(ABC):
    @abstractmethod
    async def get_my_balance(self) -> MyDomesticBalanceResponse:
        raise NotImplementedError


class KISDomesticBalanceRepository(MyBalanceRepositoryABC):
    def __init__(self, token_credential: TokenCredential):
        tr_id = "TTTC8434R" if token_credential.is_real_domain else "VTTC8434R"

        self.url = (
            token_credential.get_domain_url()
            + "/uapi/domestic-stock/v1/trading/inquire-balance"
        )

        self.kis_request_body = KISDomesticBalanceRequest(
            account_number=token_credential.get_account_number_prefix(),
            account_code=token_credential.get_account_number_suffix(),
        ).model_dump(by_alias=True)

        self.kis_request_header = KISRequestHeaderBase(
            authorization=f"{token_credential.token_type} {token_credential.access_token}",
            appkey=token_credential.appkey,
            appsecret=token_credential.appsecret,
            tr_id=tr_id,
        ).model_dump()

    async def get_my_balance(self) -> MyDomesticBalanceResponse:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params=self.kis_request_body,
                headers=self.kis_request_header,
            ) as response:
                text = await response.text()

            kis_response = KISDomesticBalanceResponse.model_validate_json(text)

            if kis_response.isSuccess() is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="국내 잔고조회 실패"
                )

            return MyDomesticBalanceResponse(
                deposit=kis_response.output2[0].dnca_tot_amt,
                deposit_next_day=kis_response.output2[0].nxdy_excc_amt,
                deposit_day_after_next=kis_response.output2[0].prvs_rcdl_excc_amt,
            )


class KISOverseasBalanceRepository(MyBalanceRepositoryABC):
    def __init__(self, token_credential: TokenCredential):
        tr_id = "TTTS3012R" if token_credential.is_real_domain else "VTTS3012R"

        self.url = (
            token_credential.get_domain_url()
            + "/uapi/overseas-stock/v1/trading/inquire-balance"
        )

        self.kis_request_body = KISOverseasBalanceRequest(
            account_number=token_credential.get_account_number_prefix(),
            account_code=token_credential.get_account_number_suffix(),
        ).model_dump(by_alias=True)

        self.kis_request_header = KISRequestHeaderBase(
            authorization=f"{token_credential.token_type} {token_credential.access_token}",
            appkey=token_credential.appkey,
            appsecret=token_credential.appsecret,
            tr_id=tr_id,
        ).model_dump()

    async def get_my_balance(self) -> MyDomesticBalanceResponse:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params=self.kis_request_body,
                headers=self.kis_request_header,
            ) as response:
                text = await response.text()

            kis_response = KISOverseasBalanceResponse.model_validate_json(text)

            if kis_response.isSuccess() is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="해외 잔고조회 실패"
                )

            return None
