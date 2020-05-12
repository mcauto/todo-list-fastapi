"""
security
"""
from typing import Optional, Any, Dict
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from starlette import status
from pydantic import BaseModel

token = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


class User(BaseModel):
    """ API를 사용하기 위한 유저 """

    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    """ User 중요 정보 """

    hashed_password: str


__fake_users_db = {
    "mcauto": {
        "username": "mcauto",
        "full_name": "Mincheol Kim",
        "email": "nexters@kakao.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    }
}


class TokenData(BaseModel):
    """ 토큰 데이터 """

    username: str


__credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="유효하지 않은 인증입니다",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> Optional[User]:
    """ 현재 요청한 유저 확인 """
    token_data = await __decode_token(token)
    if not token_data:
        raise __credential_exception
    user = await __get_user(__fake_users_db, token_data.username)
    if not user:
        raise __credential_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """ 활성화 유저 불러오기 """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def __decode_token(token: str) -> Optional[TokenData]:
    # TODO: JWT & security scope
    return TokenData(username=token)


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


__failure_sign_in_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
)


@token.post(path="")
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, Any]:
    user = await authenticate_user(
        db=__fake_users_db,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise __failure_sign_in_exception
    return {"access_token": user.username, "token_type": "bearer"}
