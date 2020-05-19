"""
파일 repo 패키지
"""
import json
from typing import Dict, List, Optional

import aiofiles
from passlib.context import CryptContext

from ..models.domain.users import UserInDB
from ..models.schemas.users import UserCreateRequest
from ..repository.base import UserRepository
from ..repository.exceptions import UserAlreadyExistException

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


class UserJSONFileRepository(UserRepository):
    """ 파일을 이용한 저장소 """

    def __init__(self, path: str):
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

    async def find_by_name(self, name: str) -> Optional[UserInDB]:
        """ name으로 user 찾기 """
        await self.__load_users()
        return self.__users.get(name, None)

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
