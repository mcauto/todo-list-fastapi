# pylint: disable=no-self-argument
"""
configuration
"""
from typing import List, Union

from pydantic import BaseSettings, HttpUrl, validator


class Settings(BaseSettings):
    """
    application 설정 (환경변수 최우선)
    """

    API_VERSION_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "have to change secret key"
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 86400 * 7
    USER_REPOSITORY_PATH: str = ""

    CORS_ALLOWS: List[HttpUrl] = []

    # sqlalchemy configuration (기본 단위 seconds)
    SQLALCHEMY_DATABASE_URL: str = ""
    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_POOL_TIMEOUT: int = 10
    SQLALCHEMY_POOL_RECYCLE: int = 3600
    SQLALCHEMY_ECHO: bool = False

    @validator("CORS_ALLOWS", pre=True)
    def __set_cors_allows(cls, v: Union[str, List[str]]) -> List[str]:  # noqa
        if isinstance(v, str) and not v.startswith("["):
            result = [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            result = v
        else:
            raise ValueError(v)
        return result

    class Config:
        """ setting의 부가 설정 """

        case_sensitive = True


settings = Settings()
