"""
routes/health.py 테스트
"""
from http import HTTPStatus


def test_health(client):
    """ test health """
    response = client.get("/api/v1/health")
    assert response.status_code == HTTPStatus.OK
