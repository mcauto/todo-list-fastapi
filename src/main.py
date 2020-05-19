"""
main.py
"""
from fastapi.applications import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from .routes import api_v1, token_router
from .core.handlers import http_exception_handler, validation_exception_handler
from .core.config import settings
from .core.database import Base, engine


def create_app() -> FastAPI:
    """ app factory method """
    app = FastAPI()
    # TODO: configuration

    app.add_exception_handler(
        RequestValidationError, handler=validation_exception_handler
    )
    app.add_exception_handler(HTTPException, handler=http_exception_handler)
    return app


Base.metadata.create_all(bind=engine)
app = create_app()
app.include_router(api_v1, prefix=f"{settings.API_VERSION_PREFIX}")
app.include_router(token_router, prefix="/api/token", tags=["auth"])
