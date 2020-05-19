from sqlalchemy import Column, text
from sqlalchemy.dialects import mysql


from .....core.database import Base
from ...constants import UserPermission


class User(Base):
    __tablename__ = "users"
    __table_args = {"mysql_collate": "utf8_general_ci"}

    username = Column("Username", mysql.VARCHAR(16), primary_key=True)
    email = Column(
        "Email",
        mysql.VARCHAR(50),
        nullable=False,
        default="",
        server_default=text("''"),
    )
    full_name = Column(
        "FullName",
        mysql.VARCHAR(32),
        nullable=False,
        default="",
        server_default=text("''"),
    )
    disabled = Column(
        "Disabled",
        mysql.TINYINT(1),
        nullable=False,
        default=0,
        server_default=text("0"),
    )
    hashed_password = Column(
        "Password",
        mysql.VARCHAR(100),
        nullable=False,
        default="",
        server_default=text("''"),
    )
    permission = Column(
        "Permission",
        mysql.TINYINT(1),
        nullable=False,
        default=0,
        server_default=text("0"),
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
        self.disabled = 1 if disabled else 0
        self.hashed_password = hashed_password
        self.permission = int(permission)
