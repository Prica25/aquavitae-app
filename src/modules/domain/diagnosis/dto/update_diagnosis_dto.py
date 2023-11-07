from datetime import date
from typing import Optional

from pydantic import BaseModel, constr, Extra

class UpdateDiagnosisDto(BaseModel):
    main: Optional[constr(max_length=1000)]
    secondary: Optional[constr(max_length=1000)]
    bowel_function: Optional[constr(max_length=1000)]
    send_by_doctor: Optional[bool]

    class Config:
        extra = Extra.forbid

