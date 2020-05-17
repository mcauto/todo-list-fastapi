from pydantic import BaseModel


class TokenData(BaseModel):
    """ 토큰 데이터 """

    username: str
