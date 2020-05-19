from typing import Optional

from pydantic import BaseModel

from ...constants import UserPermission


class User(BaseModel):
    """ API를 사용하기 위한 유저 """

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """ User 중요 정보 """

    hashed_password: str
    permission: UserPermission = UserPermission.NORMAL
