from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field

class CreateDiagnosisDto(BaseModel):
    main: constr(max_length=1000)
    secondary: Optional[constr(max_length=1000)]
    bowel_function: Optional[constr(max_length=1000)]
    send_by_doctor: Optional[bool]
    user_id: UUID = Field(alias="user")

    class Config:
        extra = Extra.forbid
