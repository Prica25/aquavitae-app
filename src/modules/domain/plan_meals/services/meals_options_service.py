from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.plan_meals.dto.meals_options.meals_options_dto import MealsOptionsDto
from src.modules.domain.plan_meals.dto.meals_options.create_meals_options_dto import CreateMealsOptionsDto
from src.modules.domain.plan_meals.dto.meals_options.update_meals_options_dto import UpdateMealsOptionsDto
from src.modules.domain.plan_meals.entities.meals_options_entity import MealsOptions
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal
from src.modules.domain.plan_meals.repositories.meals_options_repository import MealsOptionsRepository
from src.modules.domain.plan_meals.repositories.nutritional_plan_has_meal_repository import NutritionalPlanHasMealRepository

class MealsOptionsService:
    def __init__(self):
        self.meals_options_repository = MealsOptionsRepository()
        self.nutritional_plan_has_meals_repository = NutritionalPlanHasMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_meals_options(
        self, meals_options_dto: CreateMealsOptionsDto, db: Session
    ) -> Optional[MealsOptionsDto]:
        try:
            with db.begin_nested():
                nutritional_plan_has_meal = await self.nutritional_plan_has_meals_repository.find_one(
                    {
                        "where": [NutritionalPlanHasMeal.nutritional_plan_id == meals_options_dto.nutritional_plan_id, NutritionalPlanHasMeal.meals_of_plan_id == meals_options_dto.meals_of_plan_id],
                    },
                    db,
                )

                meals_options_dto.nutritional_plan_has_meal_id = nutritional_plan_has_meal.id
                delattr(meals_options_dto, "nutritional_plan_id")
                delattr(meals_options_dto, "meals_of_plan_id")
            
                new_meals_options = await self.meals_options_repository.create(meals_options_dto, db)
                
            response = MealsOptionsDto(**new_meals_options.__dict__)
            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def find_one_meals_options(self, id: str, db: Session) -> Optional[MealsOptionsDto]:
        meals_options = await self.meals_options_repository.find_one_or_fail(
            {"where": MealsOptions.id == id}, db
        )

        return MealsOptionsDto.from_orm(meals_options)

    async def delete_meals_options(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.meals_options_repository.soft_delete(id, db)

    async def update_meals_options(
        self, id: str, update_meals_options_dto: UpdateMealsOptionsDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.meals_options_repository.update(id, update_meals_options_dto, db)

    async def get_all_meals_options(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[MealsOptionsDto]]:
        [all_meals_option, total] = await self.meals_options_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [MealsOptionsDto(**meals_option.__dict__) for meals_option in all_meals_option],
            total,
            pagination["skip"],
            pagination["take"],
        )
    
    # ---------------------- PRIVATE METHODS ----------------------
    async def create_meal_option(
        self, create_meals_options_dto: CreateMealsOptionsDto, db: Session
    ) -> Optional[MealsOptionsDto]:
        new_meal_option = await self.meals_options_repository.create(create_meals_options_dto, db)

        new_meal_option = self.meals_options_repository.save(new_meal_option, db)
        return MealsOptionsDto(**new_meal_option.__dict__)