"""
conftest.py

fixture
"""
from typing import Dict, Generator
from unittest import mock

import pytest
from starlette.testclient import TestClient
from fastapi.applications import FastAPI

from src.main import create_app
from src.routes import api_v1, token_router
from src.core.config import settings
from src.apps.auth.services import create_access_token
from src.apps.auth.repository.mysql import UserMysqlRepository
from src.apps.auth.models.entity.users import User
from src.apps.auth.constants import UserPermission


@pytest.fixture
def app() -> FastAPI:
    """ test app """
    app = create_app()
    app.include_router(api_v1, prefix=f"{settings.API_VERSION_PREFIX}")
    app.include_router(token_router, prefix="/api/token")
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """ test client """
    return TestClient(app)


@pytest.fixture
def access_token() -> str:
    return create_access_token(
        username="mcauto",
        scopes=["TODO/POST", "TODO/GET", "TODO/PATCH", "TODO/DELETE"],
    )


@pytest.fixture
def authorization_headers(
    client: TestClient, access_token: str
) -> Dict[str, str]:
    """ generate token for test """
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def mock_admin() -> User:
    return User(
        username="mcauto",
        email="kmc@gabia.com",
        full_name="mcauto",
        disabled=False,
        hashed_password="$2b$12$AbbFFp9kDBqW4dAY8pAPfOD26tUNWG.S5/s4hw8nyLYl6Y2/smhy.",  # noqa
        permission=UserPermission.ADMIN,
    )


@pytest.fixture
def mocked_get_signed_user(mock_admin: User) -> Generator:  # type: ignore
    yield mock.patch.object(
        UserMysqlRepository, "_find_by_name", return_value=mock_admin
    )
