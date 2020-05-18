# pylint: disable=no-self-argument
"""
유저 스키마
"""
from typing import Dict

from pydantic import validator

from ..domain.users import User

__all__ = ["UserCreateRequest"]


class UserCreateRequest(User):
    """ 신규 계정 등록 """

    plain_password: str
    repeat_plain_password: str

    @validator("repeat_plain_password")
    def password_match(  # type: ignore
        cls, v: str, values: Dict[str, str], **kwargs  # noqa
    ) -> str:
        """ 비밀번호 확인 """
        if "plain_password" in values and v != values["plain_password"]:
            raise ValueError("password do not match")
        return v
