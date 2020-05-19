"""
유저 저장소 패키지
"""
from typing import Callable

from .base import UserRepository
from .file import UserJSONFileRepository

__all__ = ["get_users_repository", "UserRepository", "UserJSONFileRepository"]


def get_users_repository(path: str) -> Callable:  # type: ignore
    def _get_repo() -> UserRepository:
        user_repo: UserRepository = UserJSONFileRepository(path)
        return user_repo

    return _get_repo
