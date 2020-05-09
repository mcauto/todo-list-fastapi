"""
routes/health.py 테스트
"""
from http import HTTPStatus
from starlette.testclient import TestClient


def test_health(client: TestClient) -> None:
    """ test health """
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
