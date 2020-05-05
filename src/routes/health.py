"""
router
"""

from fastapi import APIRouter

health = APIRouter()


@health.get("")
async def health_check():
    """ health check """
    return {"status": "up"}
