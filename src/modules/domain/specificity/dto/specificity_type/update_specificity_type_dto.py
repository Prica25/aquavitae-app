from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class UpdateSpecificityTypeDto(BaseModel):
    description: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid