"""
exceptions
"""

from starlette import status
from fastapi.exceptions import HTTPException


CredendtialException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="유효하지 않은 인증입니다",
    headers={"WWW-Authenticate": "Bearer"},
)

FailureSignInException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
)

InactiveUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
)
