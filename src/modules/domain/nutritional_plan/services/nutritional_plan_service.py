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
from src.modules.domain.nutritional_plan.dto.nutritional_plan_dto import NutritionalPlanDto
from src.modules.domain.nutritional_plan.dto.create_nutritional_plan_dto import CreateNutritionalPlanDto
from src.modules.domain.nutritional_plan.dto.update_nutritional_plan_dto import UpdateNutritionalPlanDto
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.plan_meals.entities.nutritional_plan_has_meal_entity import NutritionalPlanHasMeal
from src.modules.domain.plan_meals.repositories.nutritional_plan_has_meal_repository import NutritionalPlanHasMealRepository
from src.modules.domain.nutritional_plan.repositories.nutritional_plan_repository import NutritionalPlanRepository
from src.modules.domain.forbidden_foods.entities.forbidden_foods_entity import ForbiddenFoods
from src.modules.domain.forbidden_foods.repositories.forbidden_foods_repository import ForbiddenFoodsRepository


class NutritionalPlanService:
    def __init__(self):
        self.nutritional_plan_repository = NutritionalPlanRepository()
        self.nutritional_plan_has_meal_repository = NutritionalPlanHasMealRepository()
        self.forbidden_foods_repository = ForbiddenFoodsRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_nutritional_plan(
        self, nutritional_plan_dto: CreateNutritionalPlanDto, db: Session
    ) -> Optional[NutritionalPlanDto]:
        try:
            with db.begin_nested():
                forbidden_foods = deepcopy(nutritional_plan_dto.forbidden_foods) if nutritional_plan_dto.forbidden_foods else []
                delattr(nutritional_plan_dto, "forbidden_foods")

                active_nutritional_plan = await self.nutritional_plan_repository.find_one(
                    {
                        "where": [NutritionalPlan.user_id == nutritional_plan_dto.user_id, NutritionalPlan.active == True],
                    },
                    db,
                )

                if active_nutritional_plan is not None:
                    await self.nutritional_plan_repository.update(
                        {"where": NutritionalPlan.id == active_nutritional_plan.id},
                        UpdateNutritionalPlanDto(active=False, user=nutritional_plan_dto.user_id),
                        db,
                    )


                new_nutritional_plan = await self.nutritional_plan_repository.create(nutritional_plan_dto, db)

                for forbidden_food in forbidden_foods:
                    ff_dto = ForbiddenFoods(
                        nutritional_plan_id=new_nutritional_plan.id, item_id=forbidden_food
                    )
                    new_nutritional_plan.forbidden_foods += [
                        await self.forbidden_foods_repository.create(ff_dto, db)
                    ]

            response = NutritionalPlanDto(**new_nutritional_plan.__dict__)
            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def get_all_nutritional_plans(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[NutritionalPlanDto]]:
        [all_nutritional_plan, total] = await self.nutritional_plan_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [NutritionalPlanDto(**nutritional_plan.__dict__) for nutritional_plan in all_nutritional_plan],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_nutritional_plan_by_id(
        self, nutritional_plan_id: str, db: Session
    ) -> Optional[NutritionalPlanDto]:
        nutritional_plan = await self.nutritional_plan_repository.find_one_or_fail(
            {
                "where": NutritionalPlan.id == nutritional_plan_id,
                "relations": ["user"],
            },
            db,
        )

        return NutritionalPlanDto(**nutritional_plan.__dict__)

    async def update_nutritional_plan(
        self,
        nutritional_plan_id: str,
        update_nutritional_plan_dto: UpdateNutritionalPlanDto,
        db: Session,
    ) -> Optional[UpdateResult]:
        try:
            with db.begin_nested():
                meals_of_plan = deepcopy(update_nutritional_plan_dto.meals_of_plan) if update_nutritional_plan_dto.meals_of_plan else []
                delattr(update_nutritional_plan_dto, "meals_of_plan")

                forbbiden_foods = deepcopy(update_nutritional_plan_dto.forbbiden_foods) if update_nutritional_plan_dto.forbbiden_foods else []
                delattr(update_nutritional_plan_dto, "forbbiden_foods")

                response = await self.nutritional_plan_repository.update(
                    {"where": NutritionalPlan.id == nutritional_plan_id},
                    update_nutritional_plan_dto,
                    db,
                )

                nutritional_plans_db = await self.nutritional_plan_has_meal_repository.find(
                    {"where": NutritionalPlanHasMeal.nutritional_plan_id == nutritional_plan_id}, db
                )

                for npm in nutritional_plans_db:
                    if npm.meals_of_plan_id not in meals_of_plan:
                        response["affected"] += (
                            await self.nutritional_plan_has_meal_repository.soft_delete(
                                str(npm.id), db
                            )
                        )["affected"]

                for npm in meals_of_plan:
                    if npm not in [
                        npm_db.meals_of_plan_id
                        for npm_db in nutritional_plans_db
                    ]:
                        npm_dto = NutritionalPlanHasMeal(
                            meals_of_plan_id=npm, nutritional_plan_id=nutritional_plan_id
                        )
                        await self.nutritional_plan_has_meal_repository.create(npm_dto, db)
                        response["affected"] += 1
                        
                forbbiden_foods_db = await self.nutritional_plan_has_meal_repository.find(
                    {"where": NutritionalPlanHasMeal.nutritional_plan_id == nutritional_plan_id}, db
                )

                for ff in forbbiden_foods_db:
                    if ff.item_id not in forbbiden_foods:
                        response["affected"] += (
                            await self.forbbiden_foods_repository.soft_delete(
                                str(ff.id), db
                            )
                        )["affected"]

                for ff in forbbiden_foods:
                    if ff not in [
                        ff_db.item_id
                        for ff_db in forbbiden_foods_db
                    ]:
                        ff_dto = ForbiddenFoods(
                            nutritional_plan_id=nutritional_plan_id, item_id=ff
                        )
                        await self.forbbiden_foods_repository.create(ff_dto, db)
                        response["affected"] += 1

            db.commit()
            return response

        except Exception as e:
            db.rollback()
            raise e

    async def delete_nutritional_plan(self, nutritional_plan_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.nutritional_plan_repository.soft_delete(nutritional_plan_id, db)

    # ---------------------- INTERFACE METHODS ----------------------
    async def find_one_nutritional_plan_by_id(
        self, nutritional_plan_id: str, db: Session
    ) -> Optional[NutritionalPlan]:
        nutritional_plan = await self.nutritional_plan_repository.find_one_or_fail(
            {
                "where": NutritionalPlan.id == nutritional_plan_id,
                "relations": ["nutritional_plan_meals"],
            },
            db,
        )

        return nutritional_plan