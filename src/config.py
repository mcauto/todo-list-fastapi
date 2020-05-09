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
    CORS_ALLOWS: List[HttpUrl] = []

    @validator("CORS_ALLOWS", pre=True)
    def __set_cors_allows(cls, v: Union[str, List[str]]) -> List[str]:  # noqa
        result = v
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
