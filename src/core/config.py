# pylint: disable=no-self-argument
"""
configuration
"""
from typing import List, Union

from pydantic import BaseSettings, HttpUrl, validator


class SQLAlchemySettings(BaseSettings):
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_ROOT_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_DATABASE: str = ""

    SQLALCHEMY_POOL_SIZE: int = 5
    SQLALCHEMY_POOL_TIMEOUT: int = 10
    SQLALCHEMY_POOL_RECYCLE: int = 3600
    SQLALCHEMY_ECHO: bool = False
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"  # noqa

    class Config:
        """ setting의 부가 설정 """

        case_sensitive = True


class Settings(BaseSettings):
    """
    application 설정 (환경변수 최우선)
    """

    API_VERSION_PREFIX: str = "/api/v1"
    PRIVATE_KEY: str = ""
    PUBLIC_KEY: str = ""
    JWT_ALGORITHM: str = "RS256"

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 86400 * 7
    USER_REPOSITORY_PATH: str = ""

    CORS_ALLOWS: List[HttpUrl] = []

    @validator("CORS_ALLOWS", pre=True)
    def __set_cors_allows(cls, v: Union[str, List[str]]) -> List[str]:  # noqa
        if isinstance(v, str) and not v.startswith("["):
            result = [i.strip() for i in v.split(",")]
        elif isinstance(v, List):
            result = v
        else:
            raise ValueError(v)
        return result

    @validator("PRIVATE_KEY", pre=True)
    def __set_private_key(cls, path: str) -> str:  # noqa
        private_key = open(path).read()
        return private_key

    @validator("PUBLIC_KEY", pre=True)
    def __set_public_key(cls, path: str) -> str:  # noqa
        public_key = open(path).read()
        return public_key

    class Config:
        """ setting의 부가 설정 """

        case_sensitive = True


settings = Settings()
sqlalchemy_settings = SQLAlchemySettings()
