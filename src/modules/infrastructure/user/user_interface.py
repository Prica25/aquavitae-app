from typing import Optional

from sqlalchemy.orm import Session

from src.core.types.find_one_options_type import FindOneOptions
from src.core.types.update_result_type import UpdateResult
from .dto.create_user_dto import CreateUserWithRoleDto
from .entities.user_entity import User
from .user_service import UserService


class UserInterface:
    def __init__(self):
        self.user_service = UserService()

    async def find_one_user(self, db: Session, find_data: FindOneOptions) -> Optional[User]:
        return await self.user_service.get_one_user(find_data, db)

    async def update_last_access(self, db: Session, id: str) -> Optional[UpdateResult]:
        return await self.user_service.update_last_access(id, db)

    async def create_user_with_role(
        self,
        user: CreateUserWithRoleDto,
        db: Session,
    ) -> Optional[User]:
        return await self.user_service.create_user(user, db)
