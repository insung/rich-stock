from fastapi import Header
from pydantic import BaseModel, Field


class KISRequestBase(BaseModel):
    account_number: str = Field(
        max_length=8,
        min_length=8,
        description="종합계좌번호. 계좌번호 체계(8-2)의 앞 8자리",
        serialization_alias="CANO",
    )
    account_code: str = Field(
        max_length=2,
        min_length=2,
        description="계좌상품코드. 계좌번호 체계(8-2)의 뒤 2자리",
        serialization_alias="ACNT_PRDT_CD",
    )


class KISResponseBase(BaseModel):
    rt_cd: int = Field(description="성공 실패 여부 (0: 성공)")
    msg_cd: str = Field(description="응답코드")
    msg1: str = Field(description="응답메세지")

    def isSuccess(self) -> bool:
        return self.rt_cd == 0


class KISRequestHeaderBase(BaseModel):
    authorization: str = Header(description="발급한 Access token")
    appkey: str = Header(description="한국투자증권 홈페이지에서 발급받은 appkey")
    appsecret: str = Header(description="한국투자증권 홈페이지에서 발급받은 appsecret")
    tr_id: str = Header(description="거래ID")
    custtype: str = Header(description="고객타입 (P: 개인 / B: 법인)", default="P")
