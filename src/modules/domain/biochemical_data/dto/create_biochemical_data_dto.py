from typing import Optional
from uuid import UUID

from pydantic import BaseModel, confloat, Extra, Field

class CreateBiochemicalDataDto(BaseModel):
    total_proteins: Optional[confloat(ge=0)]
    albumin: Optional[confloat(ge=0)]
    urea: Optional[confloat(ge=0)]
    uric_acid: Optional[confloat(ge=0)]
    creatinine: Optional[confloat(ge=0)]
    total_cholesterol: Optional[confloat(ge=0)]
    hdl: Optional[confloat(ge=0)]
    ldl: Optional[confloat(ge=0)]
    glycemia: Optional[confloat(ge=0)]
    hda1c: Optional[confloat(ge=0)]
    fasting_glycemia: Optional[confloat(ge=0)]
    post_prandial_glycemia: Optional[confloat(ge=0)]
    total_bilirubin: Optional[confloat(ge=0)]
    biliburin_direct: Optional[confloat(ge=0)]
    alkaline_phosphatase: Optional[confloat(ge=0)]
    ast_tgo: Optional[confloat(ge=0)]
    alt_tgp: Optional[confloat(ge=0)]
    ygt: Optional[confloat(ge=0)]
    appointment_id: UUID = Field(alias="appointment")

    class Config:
        extra = Extra.forbid