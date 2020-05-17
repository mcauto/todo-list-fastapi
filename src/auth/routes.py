from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from typing import Dict, Any
from fastapi.routing import APIRouter

from .services import authenticate_user, create_access_token
from .repository.fake import users
from .exceptions import FailureSignInException
from .models.domain.tokens import TokenType


token = APIRouter()


@token.post(path="")
async def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, Any]:
    user = await authenticate_user(
        db=users, username=form_data.username, password=form_data.password
    )
    if not user:
        raise FailureSignInException
    token = create_access_token(username=user.username, scopes=form_data.scopes)
    return {"access_token": token, "token_type": TokenType.BEARER}
