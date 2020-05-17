from typing import List
from pydantic import BaseModel
from enum import Enum


class TokenType(str, Enum):
    """ 토큰 타입 """

    BEARER = "bearer"


class TokenData(BaseModel):
    """ 토큰 정보 """

    username: str = ""
    scopes: List[str] = []


class TokenResponse(BaseModel):
    """ 토큰 결과 """

    access_token: str
    token_type: TokenType
