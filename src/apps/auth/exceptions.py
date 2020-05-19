"""
exceptions
"""
from typing import Dict

from fastapi.exceptions import HTTPException
from starlette import status


class CredendtialException(HTTPException):
    def __init__(self, headers: Dict[str, str] = None) -> None:
        super(CredendtialException, self).__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers=headers,
        )


FailureSignInException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Incorrect username or password",
)

InactiveUserException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="forbidden"
)
