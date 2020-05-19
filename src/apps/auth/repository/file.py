"""
파일 repo 패키지
"""
import json
from typing import Dict, List, Optional

import aiofiles

from ....core.config import settings
from ..models.domain.users import UserInDB
from ..models.schemas.users import UserCreateRequest
from ..repository.base import UserRepository
from ..repository.exceptions import (
    UserAlreadyExistException,
    UserNotFoundException,
)
from .base import get_password_hash, verify_password


class UserJSONFileRepository(UserRepository):
    """ 파일을 이용한 저장소 """

    def __init__(self, path: str = settings.USER_REPOSITORY_PATH):
        self.path: str = path
        self.__users: Dict[str, UserInDB] = {}

    async def __load_users(self) -> None:
        async with aiofiles.open(self.path, mode="r", encoding="UTF-8") as f:
            data = await f.read()
            users = json.loads(data)["users"]
            self.__users = {
                user["username"]: UserInDB(**user) for user in users
            }

    async def get_signed_user(
        self, username: str, password: str
    ) -> Optional[UserInDB]:
        user = await self.find_by_name(name=username)
        if not user:
            return None
        if not verify_password(
            input_password=password, hashed_password=user.hashed_password
        ):
            return None
        return user

    async def find_by_name(self, name: str) -> UserInDB:
        """ name으로 user 찾기 """
        await self.__load_users()
        user = self.__users.get(name, None)
        if not user:
            raise UserNotFoundException(f"{name}에 해당하는 유저를 찾지 못했습니다")
        return user

    async def insert(self, user_create_request: UserCreateRequest) -> UserInDB:
        """ 신규 유저 등록하기 """
        return await self.__insert(user_create_request)

    async def __insert(
        self, user_create_request: UserCreateRequest
    ) -> UserInDB:
        if user_create_request.username in self.__users:
            raise UserAlreadyExistException
        hashed_password = get_password_hash(user_create_request.plain_password)
        user = UserInDB(
            username=user_create_request.username,
            email=user_create_request.email,
            full_name=user_create_request.full_name,
            disabled=user_create_request.disabled,
            hashed_password=hashed_password,
        )
        self.__users[user.username] = user
        await self.__save_users()
        return user

    async def __save_users(self) -> None:
        async with aiofiles.open(self.path, mode="w", encoding="UTF-8") as f:
            user_schema_list: List[UserInDB] = [*self.__users.values()]
            user_dict_list = [user.dict() for user in user_schema_list]
            users_dict = {"users": user_dict_list}
            data = json.dumps(users_dict, ensure_ascii=False)
            await f.write(data)
            await f.flush()

    async def delete(self, username: str) -> None:
        """ 유저 제명하기"""
        await self.__delete(username=username)

    async def __delete(self, username: str) -> None:
        self.__users.pop(username)
        await self.__save_users()
