from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY


class FindAllDiagnosisQueryDto(BaseModel):
    user: Optional[constr(max_length=255)]

    class Config:
        extra = Extra.forbid


class OrderByDiagnosisQueryDto(BaseModel):
    main: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    secondary: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    bowel_function: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid
