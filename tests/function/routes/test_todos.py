"""
routes/todos.py 테스트
"""
from typing import Dict
from http import HTTPStatus
from starlette.testclient import TestClient
from src.config import settings
import pytest
import functools


@pytest.mark.parametrize(
    "method, uri, expect",
    [
        ["POST", "todos", HTTPStatus.CREATED],
        ["GET", "todos/1", HTTPStatus.OK],
        ["GET", "todos", HTTPStatus.OK],
        ["GET", "todos/7279", HTTPStatus.NOT_FOUND],
        ["PATCH", "todos/1", HTTPStatus.OK],
        ["DELETE", "todos/1", HTTPStatus.NO_CONTENT],
        ["GET", "todos", HTTPStatus.NOT_FOUND],
    ],
)
def test_todos(
    client: TestClient,
    authorization_headers: Dict[str, str],
    method: str,
    uri: str,
    expect: HTTPStatus,
) -> None:
    """ test health """
    func = {
        "GET": functools.partial(
            client.get,
            url=f"{settings.API_VERSION_PREFIX}/{uri}",
            headers=authorization_headers,
        ),
        "POST": functools.partial(
            client.post,
            url=f"{settings.API_VERSION_PREFIX}/{uri}",
            json={"title": "learning", "content": "fastapi", "is_done": False},
            headers=authorization_headers,
        ),
        "PATCH": functools.partial(
            client.patch,
            url=f"{settings.API_VERSION_PREFIX}/{uri}",
            json={"title": "study", "content": "python", "is_done": True},
            headers=authorization_headers,
        ),
        "DELETE": functools.partial(
            client.delete,
            url=f"{settings.API_VERSION_PREFIX}/{uri}",
            headers=authorization_headers,
        ),
    }
    response = func[method]()
    assert response.status_code == expect
