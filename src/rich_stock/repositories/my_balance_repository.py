from abc import ABC, abstractmethod

import aiohttp
from fastapi import HTTPException, status

from ..entities.kis_balance_entity import (
    KISBalanceRequest,
    KISBalanceRequestHeader,
    KISBalanceResponse,
)
from ..models.my_balance_model import MyBalanceResponse
from ..models.token_credential_model import TokenCredential


class MyBalanceRepositoryABC(ABC):
    @abstractmethod
    async def get_my_balance(self) -> MyBalanceResponse:
        raise NotImplementedError


class KISMyBalanceRepository(MyBalanceRepositoryABC):
    def __init__(self, token_credential: TokenCredential, is_real_domain: bool):
        tr_id = "TTTC8434R" if is_real_domain else "VTTC8434R"

        self.url = (
            token_credential.get_domain_url()
            + "/uapi/domestic-stock/v1/trading/inquire-balance"
        )

        self.kis_request_body = KISBalanceRequest(
            account_number=token_credential.get_account_number_prefix(),
            account_code=token_credential.get_account_number_suffix(),
        ).model_dump(by_alias=True)

        self.kis_request_header = KISBalanceRequestHeader(
            authorization=f"{token_credential.token_type} {token_credential.access_token}",
            appkey=token_credential.appkey,
            appsecret=token_credential.appsecret,
            tr_id=tr_id,
        ).model_dump()

    async def get_my_balance(self) -> MyBalanceResponse:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.url,
                params=self.kis_request_body,
                headers=self.kis_request_header,
            ) as response:
                text = await response.text()

            kis_response = KISBalanceResponse.model_validate_json(text)

            if kis_response.isSuccess() is False:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="잔고조회 실패"
                )

            return MyBalanceResponse(
                deposit=kis_response.output2[0].dnca_tot_amt,
                deposit_next_day=kis_response.output2[0].nxdy_excc_amt,
                deposit_day_after_next=kis_response.output2[0].prvs_rcdl_excc_amt,
            )
