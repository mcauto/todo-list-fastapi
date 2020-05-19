"""
core/errors.py 테스트
"""
from typing import Dict
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.testclient import TestClient
from src.core.config import settings


def test_http_exception_handler(
    client: TestClient, authorization_headers: Dict[str, str]
) -> None:
    """ 기본 http 예외 핸들링 테스트 """
    response = client.get(
        f"{settings.API_VERSION_PREFIX}/todos/500000",
        headers=authorization_headers,
    )
    assert response.status_code == HTTP_404_NOT_FOUND


def test_validation_exception_handler(
    client: TestClient, authorization_headers: Dict[str, str]
) -> None:
    """ 유효성 예외 핸들링 테스트 """
    response = client.get(
        f"{settings.API_VERSION_PREFIX}/todos/0", headers=authorization_headers
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
