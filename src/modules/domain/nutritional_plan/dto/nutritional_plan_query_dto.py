from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllNutritionalPlanQueryDto(BaseModel):
    active: Optional[bool]

    class Config:
        extra = Extra.forbid


class OrderByNutritionalPlanQueryDto(BaseModel):
    validate_date: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
