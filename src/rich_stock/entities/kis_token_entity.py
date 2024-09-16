from pydantic import BaseModel, Field


class KISTokenRequest(BaseModel):
    grant_type: str = Field(
        default="client_credentials",
        description="권한부여 Type",
        min_length=1,
        max_length=18,
    )

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


class KISTokenResponse(BaseModel):
    access_token: str = Field(description="접근토큰")
    token_type: str = Field(default="Bearer", description="접근토큰유형")
    expires_in: int = Field(description="접근토큰 유효기간 (초)")
    access_token_token_expired: str = Field(description="접근토큰 유효기간 (일시)")
