from uuid import UUID

from pydantic import BaseModel, Extra, Field

class CreateDiaryDto(BaseModel):
    item_id: UUID = Field(alias="item")
    nutritional_plan_has_meal_id: UUID = Field(alias="nutritional_plan_has_meal")

    class Config:
        extra = Extra.forbid
