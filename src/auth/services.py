from typing import Any, Optional

from fastapi.param_functions import Depends

from fastapi.security.oauth2 import OAuth2PasswordBearer

from .models.domain.users import UserInDB, User
from .models.domain.tokens import TokenData
from .exceptions import CredendtialException, InactiveUserException
from .repository.fake import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> Optional[User]:
    """ 현재 요청한 유저 확인 """
    token_data = await __decode_token(token)
    if not token_data:
        raise CredendtialException
    user = await __get_user(db=users, username=token_data.username)
    if not user:
        raise CredendtialException
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """ 활성화 유저 불러오기 """
    if current_user.disabled:
        raise InactiveUserException
    return current_user


async def __decode_token(token: str) -> Optional[TokenData]:
    # TODO: JWT & security scope
    return TokenData(username=token) if token else None


async def authenticate_user(
    db: Any, username: str, password: str
) -> Optional[UserInDB]:
    """ 유저 인증 """
    user = await __get_user(db=db, username=username)
    if not user:
        return None
    if not __verify_password(
        input_password=password, hashed_password=user.hashed_password
    ):
        return None
    return user


async def __get_user(db: Any, username: str) -> Optional[UserInDB]:
    user = db.get(username, None)
    if user:
        return UserInDB(**user)
    else:
        return None


def __fake_hash_password(password: str) -> str:
    return "fakehashed" + password


def __verify_password(input_password: str, hashed_password: str) -> bool:
    return __fake_hash_password(input_password) == hashed_password
