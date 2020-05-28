from sqlalchemy import Column, text
from sqlalchemy.dialects import mysql

from .....core.database import Base
from ...constants import UserPermission


class User(Base):
    __tablename__ = "users"
    __table_args = {"mysql_collate": "utf8mb4_unicode_ci"}

    username = Column(
        "Username", mysql.VARCHAR(16), primary_key=True, comment="유저ID"
    )
    email = Column(
        "Email",
        mysql.VARCHAR(50),
        nullable=False,
        default="",
        server_default=text("''"),
        comment="이메일",
    )
    full_name = Column(
        "FullName",
        mysql.VARCHAR(32),
        nullable=False,
        default="",
        server_default=text("''"),
        comment="전체 이름",
    )
    disabled = Column(
        "Disabled",
        mysql.TINYINT(1),
        nullable=True,
        default=0,
        server_default=text("0"),
        comment="사용자 활성화 여부 (0: enable, 1: disable)",
    )
    hashed_password = Column(
        "Password",
        mysql.VARCHAR(100),
        nullable=False,
        default="",
        server_default=text("''"),
        comment="비밀번호",
    )
    permission = Column(
        "Permission",
        mysql.TINYINT(1),
        nullable=False,
        default=0,
        server_default=text("0"),
        comment="유저 권한 (0: GUEST, 1: NORMAL, 2: ADMIN)",
    )

    def __init__(
        self,
        username: str,
        email: str,
        full_name: str,
        disabled: bool,
        hashed_password: str,
        permission: UserPermission,
    ) -> None:
        self.username = username
        self.email = email
        self.full_name = full_name
        self.disabled = int(disabled)
        self.hashed_password = hashed_password
        self.permission = int(permission)
