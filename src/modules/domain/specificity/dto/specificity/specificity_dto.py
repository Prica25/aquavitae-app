from typing import Optional, Union
from uuid import UUID

from pydantic import constr

from src.core.common.dto.base_dto import BaseDto
from src.modules.domain.specificity.dto.specificity_type.specificity_type_dto import SpecificityTypeDto
from src.modules.domain.food.dto.food.food_dto import FoodDto
from src.modules.infrastructure.user.dto.user_dto import UserDto

class SpecificityDto(BaseDto):
    specificity_type: Optional[Union[SpecificityTypeDto, UUID]]
    user: Optional[Union[UserDto, UUID]]
    food: Optional[Union[FoodDto, UUID]]

    def __init__(self, **kwargs):
        if "specificity_type" not in kwargs and "specificity_type_id" in kwargs:
            kwargs["specificity_type"] = kwargs["specificity_type_id"]
        if "user" not in kwargs and "user_id" in kwargs:
            kwargs["user"] = kwargs["user_id"]
        if "food" not in kwargs and "food_id" in kwargs:
            kwargs["food"] = kwargs["food_id"]
        super().__init__(**kwargs)

    class Config:
        orm_mode = True
