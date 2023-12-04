from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY

class FindAllMealsOfPlanQueryDto(BaseModel):
    nutritional_plan: Optional[constr(max_length=255)]
    class Config:
        extra = Extra.forbid


class OrderByMealsOfPlanQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    start_time: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    end_time: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
