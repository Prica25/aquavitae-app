from copy import deepcopy
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.plan_meals.dto.meals_of_plan.meals_of_plan_dto import MealsOfPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.create_meals_of_plan_dto import CreateMealsOfPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.update_meals_of_plan_dto import UpdateMealsOfPlanDto
from src.modules.domain.plan_meals.entities.meals_of_plan_entity import MealsOfPlan
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal
from src.modules.domain.plan_meals.repositories.nutritional_plan_has_meal_repository import NutritionalPlanHasMealRepository
from src.modules.domain.plan_meals.repositories.meals_of_plan_repository import MealsOfPlanRepository


class MealsOfPlanService:
    def __init__(self):
        self.meals_of_plan_repository = MealsOfPlanRepository()
        self.nutritional_plan_has_meal_repository = NutritionalPlanHasMealRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_meals_of_plan(
        self, meals_of_plan_dto: CreateMealsOfPlanDto, db: Session
    ) -> Optional[MealsOfPlanDto]:
        try:
            with db.begin_nested():
                nutritional_plans = deepcopy(meals_of_plan_dto.nutritional_plans) if meals_of_plan_dto.nutritional_plans else []
                delattr(meals_of_plan_dto, "nutritional_plans")

                new_meals_of_plan = await self.meals_of_plan_repository.create(meals_of_plan_dto, db)

                for nutritional_plan in nutritional_plans:
                    npm_dto = NutritionalPlanHasMeal(
                        meals_of_plan_id=new_meals_of_plan.id, nutritional_plan_id=nutritional_plan
                    )
                    await self.nutritional_plan_has_meal_repository.create(npm_dto, db)
                    

            response = MealsOfPlanDto(**new_meals_of_plan.__dict__)
            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def get_all_meals_of_plans(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[MealsOfPlanDto]]:
        [all_meals_of_plan, total] = await self.meals_of_plan_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [MealsOfPlanDto(**meals_of_plan.__dict__) for meals_of_plan in all_meals_of_plan],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_meals_of_plan_by_id(
        self, meals_of_plan_id: str, db: Session
    ) -> Optional[MealsOfPlanDto]:
        meals_of_plan = await self.meals_of_plan_repository.find_one_or_fail(
            {
                "where": MealsOfPlan.id == meals_of_plan_id,
                "relations": ["type_of_meal", "nutritional_plan_has_meal"],
            },
            db,
        )

        return MealsOfPlanDto(**meals_of_plan.__dict__)

    async def update_meals_of_plan(
        self,
        meals_of_plan_id: str,
        update_meals_of_plan_dto: UpdateMealsOfPlanDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        try:
            with db.begin_nested():
                nutritional_plans = (
                    deepcopy(update_meals_of_plan_dto.nutritional_plans) if update_meals_of_plan_dto.nutritional_plans else []
                )
                delattr(update_meals_of_plan_dto, "nutritional_plans")

                response = await self.meals_of_plan_repository.update(
                    {"where": MealsOfPlan.id == meals_of_plan_id},
                    update_meals_of_plan_dto,
                    db,
                )

                nutritional_plans_db = await self.nutritional_plan_has_meal_repository.find(
                    {"where": NutritionalPlanHasMeal.meals_of_plan_id == meals_of_plan_id}, db
                )

                for npm in nutritional_plans_db:
                    if npm.nutritional_plan_id not in nutritional_plans:
                        response["affected"] += (
                            await self.nutritional_plan_has_meal_repository.soft_delete(
                                str(npm.id), db
                            )
                        )["affected"]

                for npm in nutritional_plans:
                    if npm not in [
                        npm_db.nutritional_plan_id
                        for npm_db in nutritional_plans_db
                    ]:
                        npm_dto = NutritionalPlanHasMeal(
                            meals_of_plan_id=meals_of_plan_id, nutritional_plan_id=npm
                        )
                        await self.nutritional_plan_has_meal_repository.create(npm_dto, db)
                        response["affected"] += 1

            db.commit()
            return response

        except Exception as e:
            db.rollback()
            raise e

    async def delete_meals_of_plan(self, meals_of_plan_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.meals_of_plan_repository.soft_delete(meals_of_plan_id, db)
