from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED

from src.core.common.dto.pagination_response_dto import PaginationResponseDto
from src.core.constants.enum.user_role import UserRole
from src.core.decorators.http_decorator import Auth
from src.core.decorators.pagination_decorator import GetPagination
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.diary.dto.diary_dto import DiaryDto
from src.modules.domain.diary.dto.diary_query_dto import (
    FindAllDiaryQueryDto,
    OrderByDiaryQueryDto,
)
from src.modules.domain.diary.dto.create_diary_dto import CreateDiaryDto
from src.modules.domain.diary.dto.update_diary_dto import UpdateDiaryDto

from src.modules.domain.diary.entities.diary_entity import Diary
from src.modules.domain.diary.services.diary_service import DiaryService
from src.modules.infrastructure.database import get_db

diary_router = APIRouter(tags=["Diary"], prefix="/diary")

diary_service = DiaryService()


@diary_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=DiaryDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_diary(
    request: CreateDiaryDto, database: Session = Depends(get_db)
) -> Optional[DiaryDto]:
    return await diary_service.create_diary(request, database)


@diary_router.get(
    "/get",
    response_model=PaginationResponseDto[DiaryDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_diaries(
    pagination: FindManyOptions = Depends(
        GetPagination(
            Diary, DiaryDto, FindAllDiaryQueryDto, OrderByDiaryQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[DiaryDto]]:
    return await diary_service.get_all_diaries(pagination, database)


@diary_router.get(
    "/get/{diary_id}",
    response_model=DiaryDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_diary_by_id(
    diary_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[DiaryDto]:
    return await diary_service.get_diary_by_id(str(diary_id), database)


@diary_router.patch(
    "/update/{diary_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_diary(
    diary_id: UUID,
    request: UpdateDiaryDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await diary_service.update_diary(str(diary_id), request, database)


@diary_router.delete(
    "/delete/{diary_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_diary(
    diary_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await diary_service.delete_diary(str(diary_id), database)

