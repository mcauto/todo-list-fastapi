"""
main.py
"""
from fastapi import FastAPI
from .routes import api_v1


def create_app():
    """ app factory method """
    app = FastAPI()
    # TODO: configuration
    return app


app = create_app()
app.include_router(api_v1, prefix="/api/v1")
