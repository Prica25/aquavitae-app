from uuid import UUID

from pydantic import BaseModel, Extra, Field, confloat

class CreateDiaryDto(BaseModel):
    amount: confloat(ge=0.5, le=3, multiple_of=0.5) = 1.0
    item_id: UUID = Field(alias="item")
    nutritional_plan_has_meal_id: UUID = Field(alias="nutritional_plan_has_meal")

    class Config:
        extra = Extra.forbid
