from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY

class FindAllNutritionalPlanHasMealQueryDto(BaseModel):
    meals_of_plan_id: Optional[constr(max_length=255)]
    nutritional_plan_id: Optional[constr(max_length=255)]
    meal_date: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByNutritionalPlanHasMealQueryDto(BaseModel):
    meal_date: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
