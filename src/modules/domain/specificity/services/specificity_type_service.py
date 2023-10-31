from typing import List, Optional

from sqlalchemy.orm import Session

from src.core.types.exceptions_type import NotFoundException

from src.modules.domain.specificity.entities.specificity_type_entity import SpecificityType

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.specificity.dto.specificity_type.specificity_type_dto import SpecificityTypeDto
from src.modules.domain.specificity.dto.specificity_type.create_specificity_type_dto import CreateSpecificityTypeDto
from src.modules.domain.specificity.dto.specificity_type.update_specificity_type_dto import UpdateSpecificityTypeDto
from src.modules.domain.specificity.repositories.specificity_type_repository import SpecificityTypeRepository


class SpecificityTypeService:
    def __init__(self):
        self.specificity_type_repository = SpecificityTypeRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_specificity_type(
        self, specificity_type_dto: CreateSpecificityTypeDto, db: Session
    ) -> Optional[SpecificityTypeDto]:
        new_specificity_type = await self.specificity_type_repository.create(specificity_type_dto, db)

        new_specificity_type = self.specificity_type_repository.save(new_specificity_type, db)
        return SpecificityTypeDto.from_orm(new_specificity_type)

    async def find_one_specificity_type(self, id: str, db: Session) -> Optional[SpecificityTypeDto]:
        specificity_type = await self.specificity_type_repository.find_one_or_fail(
            {"where": SpecificityType.id == id}, db
        )

        return SpecificityTypeDto.from_orm(specificity_type)

    async def delete_specificity_type(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.specificity_type_repository.soft_delete(id, db)

    async def update_specificity_type(
        self, id: str, update_specificity_type_dto: UpdateSpecificityTypeDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.specificity_type_repository.update(id, update_specificity_type_dto, db)

    async def get_all_specificity_type_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[SpecificityTypeDto]]:
        [all_specificity_type, total] = await self.specificity_type_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [SpecificityTypeDto.from_orm(specificity_type) for specificity_type in all_specificity_type],
            total,
            pagination["skip"],
            pagination["take"],
        )


    # ---------------------- INTERFACE METHODS ----------------------
    async def find_one_specificity_type_by_description(
        self, description: List[str], db: Session
    ) -> Optional[List[SpecificityTypeDto]]:
        specificity_types = await self.specificity_type_repository.find(
            {
                "where": [SpecificityType.description.in_(description)],
            },
            db,
        )

        if len(specificity_types) == 0:
            raise NotFoundException(msg="No Specificity Type of any kind found")

        return [SpecificityTypeDto(**st.__dict__) for st in specificity_types]

    async def create_specificity_type(
        self, specificity_type_dto: CreateSpecificityTypeDto, db: Session
    ) -> Optional[SpecificityTypeDto]:
        new_specificity_type = await self.specificity_type_repository.create(
            specificity_type_dto, db
        )

        new_specificity_type = self.specificity_type_repository.save(new_specificity_type, db)
        return SpecificityTypeDto(**new_specificity_type.__dict__)
