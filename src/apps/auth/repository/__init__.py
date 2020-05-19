"""
유저 저장소 패키지
"""
from typing import Callable

from .base import UserRepository
from .file import UserJSONFileRepository

__all__ = ["UserRepository", "UserJSONFileRepository"]
