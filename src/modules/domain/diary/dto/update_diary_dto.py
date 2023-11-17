from typing import Optional
from uuid import UUID

from pydantic import BaseModel, confloat, Extra, Field

class UpdateDiaryDto(BaseModel):
    item_id: Optional[UUID] = Field(alias="item")
    nutritional_plan_has_meal_id: Optional[UUID] = Field(alias="nutritional_plan_has_meal")

    class Config:
        extra = Extra.forbid
