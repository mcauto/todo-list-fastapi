"""
users endpoint
"""
from fastapi import status
from fastapi.param_functions import Depends, Security
from fastapi.routing import APIRouter

from ..di.database import get_user_repository
from ..models.domain.users import User
from ..models.schemas.users import UserCreateRequest
from ..repository import UserRepository
from ..repository.mysql import UserMysqlRepository
from ..services import get_admin_user

user = APIRouter()

__admin = Security(get_admin_user)


@user.post(
    path="",
    name="회원가입",
    status_code=status.HTTP_201_CREATED,
    response_model=User,
)
async def add_user(
    user_create_request: UserCreateRequest,
    repository: UserRepository = Depends(
        get_user_repository(UserMysqlRepository)
    ),
    current_user: str = __admin,
) -> User:
    """ 회원가입 """
    user = await repository.insert(user_create_request)
    return User(**user.dict())
