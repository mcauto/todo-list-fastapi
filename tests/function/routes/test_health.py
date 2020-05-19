"""
routes/health.py 테스트
"""
from http import HTTPStatus
from starlette.testclient import TestClient
from src.core.config import settings


def test_health(client: TestClient) -> None:
    """ test health """
    response = client.get(f"{settings.API_VERSION_PREFIX}/health")
    assert response.status_code == HTTPStatus.OK
