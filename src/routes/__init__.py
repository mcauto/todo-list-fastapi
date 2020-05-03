"""
routes
"""
from fastapi import APIRouter

from .health import health

__all__ = ["api_v1"]

api_v1 = APIRouter()

api_v1.include_router(health, prefix="/health")
