from datetime import time
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field

class UpdateMealsOfPlanDto(BaseModel):
    description: Optional[constr(max_length=255)]
    start_time: Optional[time]
    end_time: Optional[time]
    type_of_meal_id: Optional[UUID] = Field(alias="type_of_meal")
    nutritional_plans: Optional[List[UUID]]

    class Config:
        extra = Extra.forbid
