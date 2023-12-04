from datetime import date
from typing import List, Optional, Union
from uuid import UUID

from pydantic import conint

from src.core.common.dto.base_dto import BaseDto
from src.core.constants.enum.periods import Periods
from src.modules.infrastructure.user.dto.user_dto import UserDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.forbidden_foods.entities.forbidden_foods_entity import ForbiddenFoods

class NutritionalPlanDto(BaseDto):
    calories_limit: Optional[conint()]
    lipids_limit: Optional[conint()]
    proteins_limit: Optional[conint()]
    carbohydrates_limit: Optional[conint()]
    period_limit: Periods
    active: bool
    validate_date: date
    user: Union[UserDto, UUID]
    forbidden_foods: Optional[Union[List[ItemDto], List[UUID]]]

    def __init__(self, **kwargs):
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]

        if (
            "forbidden_foods" in kwargs
            and kwargs["forbidden_foods"] is not None
            and len(kwargs["forbidden_foods"]) > 0
            and isinstance(kwargs["forbidden_foods"][0], ForbiddenFoods)
        ):
            kwargs["forbidden_foods"] = [
                (forbidden.item if forbidden.item else forbidden.item_id)
                for forbidden in kwargs["forbidden_foods"]
            ]

        
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
