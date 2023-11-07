from typing import Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.infrastructure.user.dto.user_dto import UserDto


class DiagnosisDto(BaseDto):
    main: constr(max_length=1000)
    secondary: Optional[constr(max_length=1000)]
    bowel_function: Optional[constr(max_length=1000)]
    send_by_doctor: Optional[bool]
    user: Optional[Union[UserDto, UUID]]

    def __init__(self, **kwargs):
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
