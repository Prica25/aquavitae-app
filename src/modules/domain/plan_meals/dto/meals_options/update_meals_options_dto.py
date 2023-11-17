from typing import Optional
from uuid import UUID

from pydantic import BaseModel, confloat, Extra, Field

class UpdateMealsOptionsDto(BaseModel):
    amount: Optional[confloat(ge=0.5, le=3, multiple_of=0.5)]
    suggested_by_system: Optional[bool]
    item_id: Optional[UUID] = Field(alias="item")
    nutritional_plan_has_meal_id: Optional[UUID] = Field(alias="nutritional_plan_has_meal")

    class Config:
        extra = Extra.forbid
