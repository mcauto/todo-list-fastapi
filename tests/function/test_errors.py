"""
core/errors.py 테스트
"""
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.testclient import TestClient


def test_http_exception_handler(client: TestClient) -> None:
    """ 기본 http 예외 핸들링 테스트 """
    response = client.get("/api/v1/todos/500000")
    assert response.status_code == HTTP_404_NOT_FOUND


def test_validation_exception_handler(client: TestClient) -> None:
    """ 유효성 예외 핸들링 테스트 """
    response = client.get("/api/v1/todos/0")
    assert response.status_code == HTTP_400_BAD_REQUEST
