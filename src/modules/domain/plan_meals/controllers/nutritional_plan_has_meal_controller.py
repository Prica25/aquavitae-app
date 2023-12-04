from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import PaginationResponseDto
from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.decorators.pagination_decorator import GetPagination
from src.core.types.find_many_options_type import FindManyOptions
from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.nutritional_plan_has_meal_dto import NutritionalPlanHasMealDto
from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.nutritional_plan_has_meal_query_dto import (
    FindAllNutritionalPlanHasMealQueryDto,
    OrderByNutritionalPlanHasMealQueryDto,
)
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal
from src.modules.domain.plan_meals.services.nutritional_plan_has_meal_service import NutritionalPlanHasMealService
from src.modules.infrastructure.database import get_db

nutritional_plan_has_meal_router = APIRouter(tags=["Nutritional Plan Has Meal"], prefix="/nutritional-plan-has-meal")

nutritional_plan_has_meal_service = NutritionalPlanHasMealService()

@nutritional_plan_has_meal_router.get(
    "/get",
    response_model=PaginationResponseDto[NutritionalPlanHasMealDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_nutritional_plan_has_meals(
    pagination: FindManyOptions = Depends(
        GetPagination(
            NutritionalPlanHasMeal, NutritionalPlanHasMealDto, FindAllNutritionalPlanHasMealQueryDto, OrderByNutritionalPlanHasMealQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[NutritionalPlanHasMealDto]]:
    return await nutritional_plan_has_meal_service.get_all_nutritional_plan_has_meals(pagination, database)