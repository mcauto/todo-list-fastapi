"""
파일 repo 패키지
"""
from typing import Optional

from ....core.database import SessionLocal
from ..models.domain.users import UserInDB
from ..models.entity.users import User
from ..models.schemas.users import UserCreateRequest
from ..repository.base import UserRepository, get_password_hash, verify_password
from ..repository.exceptions import UserNotFoundException


class UserMysqlRepository(UserRepository):
    def __init__(self) -> None:
        super(UserMysqlRepository, self).__init__()
        self.session = SessionLocal()

    async def get_signed_user(
        self, username: str, password: str
    ) -> Optional[UserInDB]:
        user = self._find_by_name(name=username)
        if not user:
            return None

        user_ = UserInDB.from_orm(user)
        if not verify_password(
            input_password=password, hashed_password=user_.hashed_password
        ):
            return None
        return user_

    async def find_by_name(self, name: str) -> UserInDB:
        user = self._find_by_name(name)
        if not user:
            raise UserNotFoundException(f"{name}에 해당하는 User를 찾지 못했습니다")
        return UserInDB.from_orm(user)

    def _find_by_name(self, name: str) -> Optional[User]:
        user: Optional[User] = self.session.query(User).filter(
            User.username == name
        ).first()
        return user

    async def insert(self, user_create_request: UserCreateRequest) -> UserInDB:
        hashed_password = get_password_hash(user_create_request.plain_password)

        user_orm = User(
            **UserInDB(
                username=user_create_request.username,
                email=user_create_request.email,
                full_name=user_create_request.full_name,
                disabled=user_create_request.disabled,
                hashed_password=hashed_password,
            ).dict()
        )
        self.session.add(user_orm)
        self.session.commit()
        self.session.refresh(user_orm)
        return UserInDB.from_orm(user_orm)

    async def delete(self, username: str) -> None:
        user = self._find_by_name(username)
        self.session.delete(user)
        self.session.commit()
