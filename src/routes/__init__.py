"""
routes
"""
from fastapi.routing import APIRouter

from .health import health as health_router
from ..todos.routes import todos as todos_router
from ..auth.routes.tokens import token as token_router
from ..auth.routes.users import user as user_router

__all__ = ["api_v1", "health_router", "todos_router", "token_router"]

api_v1 = APIRouter()


api_v1.include_router(health_router, prefix="/health", tags=["manage"])
api_v1.include_router(todos_router, prefix="/todos", tags=["todos"])
api_v1.include_router(user_router, prefix="/users", tags=["auth"])
