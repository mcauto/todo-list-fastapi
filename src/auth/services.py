import time
from typing import Iterable, List, Optional

import jwt
from fastapi.param_functions import Depends, Security
from fastapi.security.oauth2 import OAuth2PasswordBearer, SecurityScopes

from ..config import settings
from .constants import UserPermission
from .exceptions import (
    CredendtialException,
    ForbiddenException,
    InactiveUserException,
)
from .models.domain.tokens import TokenData
from .models.domain.users import User, UserInDB
from .repository import get_users_repository
from .repository.base import UserRepository

__support_scopes = {
    "TODO/POST": "create todo",
    "TODO/GET": "retrieve todo",
    "TODO/PATCH": "modify todo",
    "TODO/DELETE": "delete todo",
}

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/token", scopes=__support_scopes
)


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    repository: UserRepository = Depends(
        get_users_repository(settings.USER_REPOSITORY_PATH)
    ),
) -> Optional[User]:
    """ 현재 요청한 유저 확인 """
    credential_exception = __build_credential_exception(
        scopes=security_scopes.scope_str
    )
    token_data = await decode_token(token)
    if not token_data:
        raise credential_exception
    user = await repository.find_by_name(name=token_data.username)
    if not user:
        raise credential_exception
    if user.permission != UserPermission.ADMIN and not is_enough_permissions(
        scopes=token_data.scopes, required_scopes=security_scopes.scopes
    ):
        credential_exception.detail = "Not enough permissions"
        raise credential_exception
    return user


def __build_credential_exception(scopes: str) -> CredendtialException:
    authenticate_value = f'Bearer scope="{scopes}"' if scopes else f"Bearer"
    return CredendtialException(
        headers={"WWW-Authenticate": authenticate_value}
    )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """ 활성화 유저 불러오기 """
    if current_user.disabled:
        raise InactiveUserException
    return current_user


def get_admin_user(current_user: UserInDB = Security(get_current_user)) -> User:
    if current_user.permission != UserPermission.ADMIN:
        raise ForbiddenException
    return current_user


def create_access_token(
    username: str,
    scopes: List[str],
    expiration: int = settings.ACCESS_TOKEN_EXPIRE_SECONDS,
) -> str:
    """ 액세스 토큰 생성 (JWT) """
    iat = int(time.time())
    exp = iat + expiration
    jwt_body = {"username": username, "iat": iat, "exp": exp, "scopes": scopes}
    token = jwt.encode(jwt_body, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    return str(token, "utf-8")


async def decode_token(token: str) -> Optional[TokenData]:
    token_data: Optional[TokenData] = None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        username = payload.get("username", None)
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except jwt.PyJWTError as err:
        # TODO: logging
        token_data = None
    finally:
        return token_data


def is_enough_permissions(
    scopes: Iterable[str], required_scopes: Iterable[str]
) -> bool:
    """ permission check """
    scopes_set = set(scopes)
    required_set = set(required_scopes)
    return scopes_set.issuperset(required_set)


async def authenticate_user(
    repository: UserRepository, username: str, password: str
) -> Optional[UserInDB]:
    """ 유저 인증 """
    return await repository.get_signed_user(
        username=username, password=password
    )


async def get_user(
    repository: UserRepository, username: str
) -> Optional[UserInDB]:
    """ get user """
    return await repository.find_by_name(name=username)
