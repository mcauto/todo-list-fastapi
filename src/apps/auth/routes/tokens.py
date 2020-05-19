from typing import Any, Dict

from fastapi.param_functions import Depends
from fastapi.routing import APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from starlette import status

from ....core.config import settings
from ..exceptions import FailureSignInException
from ..models.domain.tokens import TokenType
from ..models.schemas.tokens import TokenResponse
from ..repository import UserRepository, get_users_repository
from ..services import authenticate_user, create_access_token

token = APIRouter()


@token.post(
    path="",
    name="액세스 토큰 발급",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse,
)
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    repository: UserRepository = Depends(
        get_users_repository(settings.USER_REPOSITORY_PATH)
    ),
) -> Dict[str, Any]:
    user = await authenticate_user(
        repository=repository,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise FailureSignInException
    token = create_access_token(username=user.username, scopes=form_data.scopes)
    return {"access_token": token, "token_type": TokenType.BEARER}
