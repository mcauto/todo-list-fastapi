"""
conftest.py

fixture
"""

import pytest
from fastapi.testclient import TestClient

from src.main import create_app
from src.routes import api_v1


@pytest.fixture(scope="session")
def app():
    """ test app """
    app = create_app()
    app.include_router(api_v1, prefix="/api/v1")
    return app


@pytest.fixture(scope="session")
def client(app):
    """ test client """
    yield TestClient(app)
