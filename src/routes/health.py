"""
router
"""
from typing import Dict
from fastapi.routing import APIRouter

health = APIRouter()


@health.get("")
async def health_check() -> Dict[str, str]:
    """ health check """
    return {"status": "up"}
