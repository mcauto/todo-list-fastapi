"""
routes/token.py 테스트
"""
from typing import Generator
import pytest

from starlette.testclient import TestClient
from starlette import status
from fastapi.security.oauth2 import SecurityScopes
from starlette.exceptions import HTTPException
from src.apps.auth.services import (
    get_current_active_user,
    create_access_token,
    get_current_user,
)
from src.apps.auth.models.domain.users import User
from src.apps.auth.repository import UserJSONFileRepository, UserRepository
from src.core.exceptions import RepositoryException
from src.core.config import settings


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
    "token, scopes, repository",
    [
        [
            create_access_token(username="mcauto", scopes=[]),
            SecurityScopes(),
            UserJSONFileRepository(settings.USER_REPOSITORY_PATH),
        ]
    ],
)
async def test_get_current_user(
    scopes: SecurityScopes, token: str, repository: UserRepository
) -> None:
    try:
        await get_current_user(
            security_scopes=scopes, token=token, repository=repository
        )
    except HTTPException:
        assert False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token, scopes, repository",
    [
        [
            create_access_token(username="unknown", scopes=[]),
            SecurityScopes(),
            UserJSONFileRepository(settings.USER_REPOSITORY_PATH),
        ]
    ],
)
async def test_get_current_user_not_exist(
    scopes: SecurityScopes, token: str, repository: UserRepository
) -> None:
    try:
        await get_current_user(
            security_scopes=scopes, token=token, repository=repository
        )
    except (HTTPException, RepositoryException):
        pass
    else:
        assert False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token, scopes, repository",
    [
        [
            "",
            SecurityScopes(),
            UserJSONFileRepository(settings.USER_REPOSITORY_PATH),
        ]
    ],
)
async def test_get_current_user_decode_fail(
    scopes: SecurityScopes, token: str, repository: UserRepository
) -> None:
    try:
        await get_current_user(
            security_scopes=scopes, token=token, repository=repository
        )
    except (HTTPException, RepositoryException):
        pass
    else:
        assert False


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
