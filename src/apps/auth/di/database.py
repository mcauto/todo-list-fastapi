from typing import Callable, Type

from ....core.database import SessionLocal
from ..repository.base import UserRepository


# Dependency
def get_db():  # type: ignore
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(
    repository_type: Type[UserRepository]
) -> Callable:  # type: ignore
    def _get_repo() -> UserRepository:
        return repository_type()

    return _get_repo
