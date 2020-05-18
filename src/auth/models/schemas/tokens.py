from pydantic import BaseModel

from ..domain.tokens import TokenType


class TokenResponse(BaseModel):
    """ 토큰 결과 """

    access_token: str
    token_type: TokenType
