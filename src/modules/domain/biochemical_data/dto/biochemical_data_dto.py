from typing import Optional, Union
from uuid import UUID

from pydantic import confloat

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.appointment.dto.appointment.appointment_dto import AppointmentDto

class BiochemicalDataDto(BaseDto):
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
    appointment: Optional[Union[AppointmentDto, UUID]]

    def __init__(self, **kwargs):
        if "appointment" not in kwargs and "appointment_id" in kwargs:
            kwargs["appointment"] = kwargs["appointment_id"]

        super().__init__(**kwargs)

    class Config:
        orm_mode = True
