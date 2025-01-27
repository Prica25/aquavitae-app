from datetime import datetime
from typing import Optional

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.user_role import UserRole


class UserDto(BaseDto):
    email: str
    role: UserRole
    last_access: Optional[datetime]
    profile_photo: Optional[bytes]

    class Config:
        orm_mode = True
