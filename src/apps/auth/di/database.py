from typing import Callable, Type

from ..repository.base import UserRepository


def get_user_repository(
    repository_type: Type[UserRepository]
) -> Callable:  # type: ignore
    def _get_repo() -> UserRepository:
        return repository_type()

    return _get_repo
