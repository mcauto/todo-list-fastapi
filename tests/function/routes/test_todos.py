"""
routes/todos.py 테스트
"""
from http import HTTPStatus
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
def test_todos(client, method, uri, expect):
    """ test health """
    func = {
        "GET": functools.partial(client.get, url=f"/api/v1/{uri}"),
        "POST": functools.partial(
            client.post,
            url=f"/api/v1/{uri}",
            json={"title": "learning", "content": "fastapi", "is_done": False},
        ),
        "PATCH": functools.partial(
            client.patch,
            url=f"/api/v1/{uri}",
            json={"title": "study", "content": "python", "is_done": True},
        ),
        "DELETE": functools.partial(client.delete, url=f"/api/v1/{uri}"),
    }
    response = func[method]()
    assert response.status_code == expect
