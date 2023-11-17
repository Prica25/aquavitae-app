from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.diary.dto.diary_dto import DiaryDto
from src.modules.domain.diary.dto.create_diary_dto import CreateDiaryDto
from src.modules.domain.diary.dto.update_diary_dto import UpdateDiaryDto
from src.modules.domain.diary.entities.diary_entity import Diary
from src.modules.domain.diary.repositories.diary_repository import DiaryRepository

class DiaryService:
    def __init__(self):
        self.diary_repository = DiaryRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_diary(
        self, diary_dto: CreateDiaryDto, db: Session
    ) -> Optional[DiaryDto]:
        new_diary = await self.diary_repository.create(diary_dto, db)

        new_diary = self.diary_repository.save(new_diary, db)
        return DiaryDto.from_orm(new_diary)

    async def find_one_diary(self, id: str, db: Session) -> Optional[DiaryDto]:
        diary = await self.diary_repository.find_one_or_fail(
            {"where": Diary.id == id}, db
        )

        return DiaryDto.from_orm(diary)

    async def delete_diary(self, id: str, db: Session) -> Optional[UpdateResult]:
        return await self.diary_repository.soft_delete(id, db)

    async def update_diary(
        self, id: str, update_diary_dto: UpdateDiaryDto, db: Session
    ) -> Optional[UpdateResult]:
        return await self.diary_repository.update(id, update_diary_dto, db)

    async def get_all_diary_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[DiaryDto]]:
        [all_diary, total] = await self.diary_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [DiaryDto.from_orm(diary) for diary in all_diary],
            total,
            pagination["skip"],
            pagination["take"],
        )
