"""
routes/todos.py 테스트
"""
from typing import Dict, Generator
from http import HTTPStatus
from starlette.testclient import TestClient
from src.core.config import settings
import pytest
import functools


@pytest.mark.parametrize(
    "method, uri, expect",
    [
        ["GET", "todos", HTTPStatus.NOT_FOUND],
        ["POST", "todos", HTTPStatus.CREATED],
        ["GET", "todos/1", HTTPStatus.OK],
        ["GET", "todos", HTTPStatus.OK],
        ["GET", "todos/7279", HTTPStatus.NOT_FOUND],
        ["PATCH", "todos/1", HTTPStatus.OK],
        ["PATCH", "todos/2", HTTPStatus.NOT_FOUND],
        ["DELETE", "todos/1", HTTPStatus.NO_CONTENT],
        ["DELETE", "todos/2", HTTPStatus.NOT_FOUND],
        ["GET", "todos", HTTPStatus.NOT_FOUND],
    ],
)
def test_todos(
    client: TestClient,
    authorization_headers: Dict[str, str],
    method: str,
    uri: str,
    expect: HTTPStatus,
    mocked_get_signed_user: Generator,  # type: ignore
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
    with mocked_get_signed_user:  # type: ignore
        response = func[method]()
        assert response.status_code == expect
