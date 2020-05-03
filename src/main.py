"""
main.py
"""
import time

from fastapi import FastAPI
from .routes import health


def create_app():
    """ app factory method """
    app = FastAPI()
    # TODO: configuration

    # add routes
    app.include_router(health, prefix="/health")
    return app


app = create_app()
