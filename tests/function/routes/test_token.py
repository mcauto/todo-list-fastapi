"""
routes/token.py 테스트
"""
from typing import Generator
import pytest

from starlette.testclient import TestClient
from starlette import status
from starlette.exceptions import HTTPException
from src.apps.auth.services import get_current_active_user
from src.apps.auth.models.domain.users import User
from src.core.exceptions import RepositoryException


@pytest.mark.parametrize(
    "username, password, expect",
    [
        ["mcauto", "imdeo", status.HTTP_201_CREATED],
        ["mcauto", "wrong_secret", status.HTTP_400_BAD_REQUEST],
    ],
)
def test_sign_in(
    client: TestClient,
    username: str,
    password: str,
    expect: int,
    mocked_get_signed_user: Generator,  # type: ignore
) -> None:
    with mocked_get_signed_user:  # type: ignore
        response = client.post(
            url="/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"username": username, "password": password},
        )
        assert response.status_code == expect


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "current_user", [User(username="mcauto", disabled=True)]
)
async def test_get_current_active_user(current_user: User) -> None:
    try:
        await get_current_active_user(current_user)
    except (HTTPException, RepositoryException):
        pass
    else:
        assert False
