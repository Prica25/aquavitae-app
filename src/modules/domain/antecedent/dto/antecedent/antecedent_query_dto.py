from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllAntecedentQueryDto(BaseModel):
    description: Optional[constr(max_length=255)]
    user_id: Optional[UUID]

    class Config:
        extra = Extra.forbid


class OrderByAntecedentQueryDto(BaseModel):
    description: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
