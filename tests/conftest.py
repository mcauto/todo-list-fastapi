"""
conftest.py

fixture
"""

import pytest
from starlette.testclient import TestClient
from fastapi.applications import FastAPI

from src.main import create_app
from src.routes import api_v1
from src.config import settings


@pytest.fixture
def app() -> FastAPI:
    """ test app """
    app = create_app()
    app.include_router(api_v1, prefix=f"{settings.API_VERSION_PREFIX}")
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """ test client """
    return TestClient(app)
