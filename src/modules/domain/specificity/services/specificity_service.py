from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.specificity.dto.specificity.specificity_dto import SpecificityDto
from src.modules.domain.specificity.dto.specificity.create_specificity_dto import CreateSpecificityDto
from src.modules.domain.specificity.dto.specificity.update_specificity_dto import UpdateSpecificityDto
from src.modules.domain.specificity.entities.specificity_entity import Specificity
from src.modules.domain.specificity.repositories.specificity_repository import SpecificityRepository


class SpecificityService:
    def __init__(self):
        self.specificity_repository = SpecificityRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_specificity(
        self, specificity_dto: CreateSpecificityDto, db: Session
    ) -> Optional[SpecificityDto]:
        new_specificity = await self.specificity_repository.create(specificity_dto, db)

        new_specificity = self.specificity_repository.save(new_specificity, db)
        return SpecificityDto.from_orm(new_specificity)

    async def find_one_specificity(self, id: str, db: Session) -> Optional[SpecificityDto]:
        specificity = await self.specificity_repository.find_one_or_fail(
            {"where": Specificity.id == id}, db
        )

        return SpecificityDto.from_orm(specificity)

    async def delete_specificity(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.specificity_repository.soft_delete(id, db)

    async def update_specificity(
        self, id: str, update_specificity_dto: UpdateSpecificityDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.specificity_repository.update(id, update_specificity_dto, db)

    async def get_all_specificity_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[SpecificityDto]]:
        [all_specificity, total] = await self.specificity_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [SpecificityDto.from_orm(specificity) for specificity in all_specificity],
            total,
            pagination["skip"],
            pagination["take"],
        )
