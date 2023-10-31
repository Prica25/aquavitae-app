from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class UpdateSpecificityDto(BaseModel):
    description: Optional[constr(max_length=255)]
    specificity_type_id: Optional[UUID] = Field(alias="specificity_type")
    food_id: Optional[UUID] = Field(alias="food")

    class Config:
        extra = Extra.forbid
