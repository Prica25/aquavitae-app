from typing import Optional

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY

class FindAllDiaryQueryDto(BaseModel):
    class Config:
        extra = Extra.forbid


class OrderByDiaryQueryDto(BaseModel):
    class Config:
        extra = Extra.forbid
