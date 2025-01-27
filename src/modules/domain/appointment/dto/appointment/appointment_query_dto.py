from typing import Optional

from pydantic import BaseModel, constr, Extra, Field

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllAppointmentQueryDto(BaseModel):
    date: Optional[constr()]
    status: Optional[constr()]
    user_id: Optional[constr()]
    nutritionist_id: Optional[constr()]

    class Config:
        extra = Extra.forbid


class OrderByAppointmentQueryDto(BaseModel):
    date: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    status: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
