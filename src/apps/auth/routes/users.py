"""
users endpoint
"""
from fastapi import status
from fastapi.param_functions import Depends, Security
from fastapi.routing import APIRouter

from ....core.config import settings
from ..models.domain.users import User
from ..models.schemas.users import UserCreateRequest
from ..repository import UserRepository, get_users_repository
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
        get_users_repository(settings.USER_REPOSITORY_PATH)
    ),
    current_user: str = __admin,
) -> User:
    """ 회원가입 """
    user = await repository.insert(user_create_request)
    return User(**user.dict())
