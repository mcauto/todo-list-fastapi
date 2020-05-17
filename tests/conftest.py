"""
conftest.py

fixture
"""
from typing import Dict

import pytest
from starlette.testclient import TestClient
from fastapi.applications import FastAPI

from src.main import create_app
from src.routes import api_v1, token_router
from src.config import settings
from src.auth.services import create_access_token


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
