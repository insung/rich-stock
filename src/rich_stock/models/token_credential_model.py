from typing import Self

from ..entities.kis_token_entity import KISTokenResponse
from ..models.token_model import TokenIssueRequest


class TokenCredential(TokenIssueRequest, KISTokenResponse):
    @classmethod
    def from_model(
        cls,
        token_issue_request: TokenIssueRequest,
        kis_token_response: KISTokenResponse,
    ) -> Self:
        token_credential = {
            **token_issue_request.model_dump(),
            **kis_token_response.model_dump(),
        }

        return TokenCredential(**token_credential)
