from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.param_functions import Depends
from typing import Dict, Any
from fastapi.routing import APIRouter

from .services import authenticate_user
from .repository.fake import users
from .exceptions import FailureSignInException


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
    return {"access_token": user.username, "token_type": "bearer"}
