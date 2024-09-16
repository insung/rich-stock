import os
from pydantic import BaseModel, Field


class TokenIssueRequest(BaseModel):
    appkey: str = Field(
        description="한국투자증권 홈페이지에서 발급받은 appkey",
        min_length=1,
        max_length=36,
    )
    appsecret: str = Field(
        description="한국투자증권 홈페이지에서 발급받은 appsecret",
        min_length=1,
        max_length=180,
    )
    account_number: str = Field(
        description="계좌번호 (8-2)",
        min_length=11,
        max_length=11,
        examples=["00000000-00"],
    )
    is_real_domain: bool = Field(description="실전 도메인 여부")

    def get_domain_url(self) -> str:
        if self.is_real_domain:
            return os.environ.get("real_domain")
        else:
            return os.environ.get("mock_domain")

    def get_account_number_prefix(self) -> str:
        return self.account_number.split("-")[0]

    def get_account_number_suffix(self) -> str:
        return self.account_number.split("-")[1]


class TokenIssueResponse(BaseModel):
    token: str = Field(description="인증토큰")
    expired: str = Field(description="접근토큰 유효기간 (일시)")
