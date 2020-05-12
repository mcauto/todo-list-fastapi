"""
routes
"""
from fastapi.routing import APIRouter

from .health import health as health_router
from .todos import todos as todos_router
from .token import token as token_router

__all__ = ["api_v1", "health_router", "todos_router", "token_router"]

api_v1 = APIRouter()


api_v1.include_router(health_router, prefix="/health", tags=["manage"])
api_v1.include_router(todos_router, prefix="/todos", tags=["todos"])
