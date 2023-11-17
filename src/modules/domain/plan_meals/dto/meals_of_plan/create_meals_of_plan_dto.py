from uuid import UUID
from typing import List, Optional
from datetime import time

from pydantic import BaseModel, constr, Extra, Field

class CreateMealsOfPlanDto(BaseModel):
    description: constr(max_length=255)
    start_time: time
    end_time: time
    type_of_meal_id: UUID = Field(alias="type_of_meal")
    nutritional_plans: Optional[List[UUID]]

    class Config:
        extra = Extra.forbid
