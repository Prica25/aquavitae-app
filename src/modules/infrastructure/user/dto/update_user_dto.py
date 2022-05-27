from typing import Optional

from pydantic import BaseModel, constr, EmailStr


class UpdateUserDto(BaseModel):
    name: Optional[constr(min_length=2, max_length=255)]
    email: Optional[EmailStr]
    password: Optional[str]
