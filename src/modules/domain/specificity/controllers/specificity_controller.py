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
from src.modules.domain.specificity.dto.specificity.specificity_dto import SpecificityDto
from src.modules.domain.specificity.dto.specificity.specificity_query_dto import (
    FindAllSpecificityQueryDto,
    OrderBySpecificityQueryDto,
)
from src.modules.domain.specificity.dto.specificity.create_specificity_dto import CreateSpecificityDto
from src.modules.domain.specificity.dto.specificity.update_specificity_dto import UpdateSpecificityDto
from src.modules.domain.specificity.entities.specificity_entity import Specificity
from src.modules.domain.specificity.services.specificity_service import SpecificityService
from src.modules.infrastructure.database import get_db

specificity_router = APIRouter(tags=["Specificity"], prefix="/specificity")

specificity_service = SpecificityService()


@specificity_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=SpecificityDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_specificity(
    request: CreateSpecificityDto, database: Session = Depends(get_db)
) -> Optional[SpecificityDto]:
    return await specificity_service.create_specificity(request, database)


@specificity_router.get(
    "/get/{id}",
    response_model=SpecificityDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_specificity_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[SpecificityDto]:
    return await specificity_service.find_one_specificity(str(id), database)


@specificity_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_specificity(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await specificity_service.delete_specificity(str(id), database)


@specificity_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_specificity(
    request: UpdateSpecificityDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await specificity_service.update_specificity(str(id), request, database)


@specificity_router.get(
    "/get",
    response_model=PaginationResponseDto[SpecificityDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_specificity_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            Specificity,
            SpecificityDto,
            FindAllSpecificityQueryDto,
            OrderBySpecificityQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[SpecificityDto]]:
    return await specificity_service.get_all_specificity_paginated(pagination, database)
