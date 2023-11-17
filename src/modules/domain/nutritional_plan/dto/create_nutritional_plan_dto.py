from uuid import UUID
from typing import List, Optional
from datetime import date

from src.core.constants.enum.periods import Periods
from pydantic import BaseModel, conint, Extra, Field

class CreateNutritionalPlanDto(BaseModel):
    calories_limit: Optional[conint()]
    lipids_limit: Optional[conint()]
    proteins_limit: Optional[conint()]
    carbohydrates_limit: Optional[conint()]
    period_limit: Periods
    active: bool
    validate_date: date
    user_id: UUID = Field(alias="user")
    meals_of_plan: Optional[List[UUID]]
    forbidden_foods: Optional[List[UUID]]

    class Config:
        extra = Extra.forbid
