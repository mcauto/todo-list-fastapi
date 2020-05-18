"""
base repository
"""
from abc import ABCMeta, abstractmethod
from typing import Optional

from ..models.domain.users import UserInDB
from ..models.schemas.users import UserCreateRequest


class UserRepository(metaclass=ABCMeta):
    """ 수집 장비 저장소 """

    @abstractmethod
    async def get_signed_user(
        self, username: str, password: str
    ) -> Optional[UserInDB]:
        """ sign in """

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[UserInDB]:
        """ name으로 user 찾기 """

    @abstractmethod
    async def insert(self, user_create_request: UserCreateRequest) -> UserInDB:
        """ 신규 유저 등록하기 """

    @abstractmethod
    async def delete(self, username: str) -> None:
        """ 유저 제명하기"""
