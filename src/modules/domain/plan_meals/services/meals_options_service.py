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
from src.modules.domain.plan_meals.repositories.meals_options_repository import MealsOptionsRepository

class MealsOptionsService:
    def __init__(self):
        self.meals_options_repository = MealsOptionsRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_meals_options(
        self, meals_options_dto: CreateMealsOptionsDto, db: Session
    ) -> Optional[MealsOptionsDto]:
        new_meals_options = await self.meals_options_repository.create(meals_options_dto, db)

        new_meals_options = self.meals_options_repository.save(new_meals_options, db)
        return MealsOptionsDto.from_orm(new_meals_options)

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

    async def get_all_meals_options_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[MealsOptionsDto]]:
        [all_meals_options, total] = await self.meals_options_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [MealsOptionsDto.from_orm(meals_options) for meals_options in all_meals_options],
            total,
            pagination["skip"],
            pagination["take"],
        )
