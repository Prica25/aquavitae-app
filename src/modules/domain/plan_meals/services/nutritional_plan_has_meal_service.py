from datetime import date
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions

from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.create_nutritional_plan_has_meal_dto import (
    CreateNutritionalPlanHasMealDto,
)
from src.modules.domain.plan_meals.dto.nutritional_plan_has_meal.nutritional_plan_has_meal_dto import (
    NutritionalPlanHasMealDto,
)
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import (
    NutritionalPlanHasMeal,
)
from src.modules.domain.plan_meals.repositories.nutritional_plan_has_meal_repository import (
    NutritionalPlanHasMealRepository,
)


class NutritionalPlanHasMealService:
    def __init__(self):
        self.nphm_repository = NutritionalPlanHasMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_nutritional_plan_has_meal(
        self, create_nphm_dto: CreateNutritionalPlanHasMealDto, db: Session
    ) -> Optional[NutritionalPlanHasMealDto]:
        new_nphm = await self.nphm_repository.create(create_nphm_dto, db)

        new_nphm = self.nphm_repository.save(new_nphm, db)
        return NutritionalPlanHasMealDto(**new_nphm.__dict__)
    
    async def get_all_nutritional_plan_has_meals(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[NutritionalPlanHasMealDto]]:
        [all_nutritional_plan_has_meals, total] = await self.nphm_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [NutritionalPlanHasMealDto(**nutritional_plan_has_meal.__dict__) for nutritional_plan_has_meal in all_nutritional_plan_has_meals],
            total,
            pagination["skip"],
            pagination["take"],
        )

    # ---------------------- INTERFACE METHODS ----------------------
    async def get_nutritional_plan_has_meal_by_date(
        self, meal_date: date, nutritional_plan_id: UUID, meal_of_plan_id: UUID, db: Session
    ) -> Optional[NutritionalPlanHasMealDto]:
        result = await self.nphm_repository.find_one_or_fail(
            {
                "where": [
                    NutritionalPlanHasMeal.meal_date == meal_date,
                    NutritionalPlanHasMeal.nutritional_plan_id == nutritional_plan_id,
                    NutritionalPlanHasMeal.meals_of_plan_id == meal_of_plan_id,
                ]
            },
            db,
        )

        return NutritionalPlanHasMealDto.from_orm(result)
