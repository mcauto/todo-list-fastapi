"""
config 테스트
"""
import os
from src.config import Settings
from pydantic import HttpUrl
from pydantic.env_settings import SettingsError
import pytest


@pytest.mark.parametrize(
    "urls",
    [
        '"http://127.0.0.1"',
        '["http://127.0.0.1"]',
        '"http://127.0.0.1, http://172.26.22.2"',
        '["http://127.0.0.1","http://172.26.22.2"]',
    ],
)
def test_set_cors_allows(urls: str) -> None:
    os.environ["CORS_ALLOWS"] = urls
    try:
        settings = Settings()
    except SettingsError as err:
        assert False
    else:
        assert True


def test_set_cors_allows_failure() -> None:
    os.environ["CORS_ALLOWS"] = "2130706433"  # 127.0.0.1
    try:
        settings = Settings()
    except ValueError:
        assert True
    else:
        assert False
