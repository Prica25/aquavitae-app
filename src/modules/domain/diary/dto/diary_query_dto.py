from typing import Optional

from pydantic import BaseModel, constr, Extra

class FindAllDiaryQueryDto(BaseModel):
    nutritional_plan_has_meal_id: Optional[constr(max_length=255)]
    class Config:
        extra = Extra.forbid


class OrderByDiaryQueryDto(BaseModel):
    class Config:
        extra = Extra.forbid
