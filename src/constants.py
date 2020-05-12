"""
constants
"""
from enum import IntEnum


class UserPermission(IntEnum):
    """ 유저 권한 """

    GUEST = 0
    NORMAL = 1
    ADMIN = 2
