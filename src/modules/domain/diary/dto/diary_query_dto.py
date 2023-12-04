from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllDiaryQueryDto(BaseModel):
    nutritional_plan_has_meal_id: Optional[constr(max_length=255)]
    class Config:
        extra = Extra.forbid


class OrderByDiaryQueryDto(BaseModel):
    amount: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
