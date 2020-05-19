from enum import Enum
from typing import List

from pydantic import BaseModel


class TokenType(str, Enum):
    """ 토큰 타입 """

    BEARER = "bearer"


class TokenData(BaseModel):
    """ 토큰 정보 """

    username: str = ""
    scopes: List[str] = []
