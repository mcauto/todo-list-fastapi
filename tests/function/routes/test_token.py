"""
routes/token.py 테스트
"""
import pytest

from starlette.testclient import TestClient
from starlette import status
from fastapi.security.oauth2 import SecurityScopes
from starlette.exceptions import HTTPException
from src.auth.services import (
    get_current_active_user,
    create_access_token,
    get_current_user,
)
from src.auth.models.domain.users import User


@pytest.mark.parametrize(
    "username, password, expect",
    [
        ["mcauto", "secret", status.HTTP_200_OK],
        ["mcauto", "wrong_secret", status.HTTP_400_BAD_REQUEST],
        ["unknown", "secret", status.HTTP_400_BAD_REQUEST],
    ],
)
def test_sign_in(
    client: TestClient, username: str, password: str, expect: int
) -> None:
    response = client.post(
        url="/api/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )
    assert response.status_code == expect


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token, scopes",
    [[create_access_token(username="mcauto", scopes=[]), SecurityScopes()]],
)
async def test_get_current_user(scopes: SecurityScopes, token: str) -> None:
    try:
        await get_current_user(security_scopes=scopes, token=token)
    except HTTPException:
        assert False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "token, scopes",
    [[create_access_token(username="unknown", scopes=[]), SecurityScopes()]],
)
async def test_get_current_user_not_exist(
    scopes: SecurityScopes, token: str
) -> None:
    try:
        await get_current_user(security_scopes=scopes, token=token)
    except HTTPException:
        pass
    else:
        assert False


@pytest.mark.asyncio
@pytest.mark.parametrize("token, scopes", [["", SecurityScopes()]])
async def test_get_current_user_decode_fail(
    scopes: SecurityScopes, token: str
) -> None:
    try:
        await get_current_user(security_scopes=scopes, token=token)
    except HTTPException:
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
    except HTTPException:
        pass
    else:
        assert False
