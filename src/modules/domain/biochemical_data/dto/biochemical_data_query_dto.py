from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr, Extra

from src.core.constants.regex_expressions import REGEX_ORDER_BY_QUERY

class FindAllBiochemicalDataQueryDto(BaseModel):
    appointment_id: UUID

    class Config:
        extra = Extra.forbid

class OrderByBiochemicalDataQueryDto(BaseModel):
    total_proteins: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    albumin: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    urea: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    uric_acid: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    creatinine: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    total_cholesterol: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    hdl: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    ldl: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    glycemia: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    hda1c: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    fasting_glycemia: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    post_prandial_glycemia: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    total_bilirubin: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    biliburin_direct: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    alkaline_phosphatase: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    ast_tgo: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    alt_tgp: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]
    ygt: Optional[constr(regex=REGEX_ORDER_BY_QUERY)]

    class Config:
        extra = Extra.forbid