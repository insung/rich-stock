from datetime import datetime
import os
import aiohttp
from fastapi import APIRouter, Security, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from ..entities.kis_token_entity import KISTokenRequest, KISTokenResponse
from ..models.token_credential_model import TokenCredential
from ..models.token_model import (
    TokenIssueResponse,
    TokenIssueRequest,
)


auth_router = APIRouter(prefix="/auth", tags=["Auth"])
api_key = os.environ.get("api_key")


@auth_router.post("/issue_token", description="토큰발급")
async def issue_token(body: TokenIssueRequest) -> TokenIssueResponse:
    url = body.get_domain_url() + "/oauth2/tokenP"
    kis_request = KISTokenRequest(appkey=body.appkey, appsecret=body.appsecret)
    data = kis_request.model_dump_json()
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            text = await response.text()
            if "error_code" in text:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail=text
                )

            kis_token_response = KISTokenResponse.model_validate_json(text)
            payload = TokenCredential.from_model(
                token_issue_request=body, kis_token_response=kis_token_response
            ).model_dump()
            token = jwt.encode(payload, api_key, algorithm="HS256")
            return TokenIssueResponse(
                token=token, expired=kis_token_response.access_token_token_expired
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> TokenCredential:
    credential = credentials.credentials
    decode = jwt.decode(credential, api_key, algorithms="HS256")
    token_credential = TokenCredential.model_validate(decode)
    access_token_expired = datetime.strptime(
        token_credential.access_token_token_expired, "%Y-%m-%d %H:%M:%S"
    )

    if datetime.now() > access_token_expired:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="access_token was expired."
        )

    return token_credential
