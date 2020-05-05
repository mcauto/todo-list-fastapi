"""
routes
"""
from fastapi import APIRouter

from .health import health
from .todos import todos

__all__ = ["api_v1"]

api_v1 = APIRouter()

api_v1.include_router(health, prefix="/health")
api_v1.include_router(todos, prefix="/todos")
