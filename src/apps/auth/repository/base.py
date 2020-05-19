"""
base repository
"""
from abc import ABCMeta, abstractmethod
from typing import Optional

from passlib.context import CryptContext

from ..models.domain.users import UserInDB
from ..models.schemas.users import UserCreateRequest

__pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(input_password: str, hashed_password: str) -> bool:
    try:
        verify: bool = __pwd_context.verify(input_password, hashed_password)
    except (ValueError, RuntimeError) as err:
        print(err)
        verify = False
    finally:
        return verify


def get_password_hash(password: str) -> str:
    """ password hash """
    hashed_password = __pwd_context.hash(password)
    return str(hashed_password)


class UserRepository(metaclass=ABCMeta):
    """ 수집 장비 저장소 """

    @abstractmethod
    async def get_signed_user(
        self, username: str, password: str
    ) -> Optional[UserInDB]:
        """ sign in """

    @abstractmethod
    async def find_by_name(self, name: str) -> UserInDB:
        """ name으로 user 찾기 """

    @abstractmethod
    async def insert(self, user_create_request: UserCreateRequest) -> UserInDB:
        """ 신규 유저 등록하기 """

    @abstractmethod
    async def delete(self, username: str) -> None:
        """ 유저 제명하기"""
