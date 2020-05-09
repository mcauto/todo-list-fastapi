"""
routes
"""
from fastapi.routing import APIRouter

from .health import health as health_router
from .todos import todos as todos_router

__all__ = ["api_v1", "health_router", "todos_router"]

api_v1 = APIRouter()

api_v1.include_router(health_router, prefix="/health")
api_v1.include_router(todos_router, prefix="/todos")
