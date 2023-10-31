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
from src.modules.domain.specificity.dto.specificity_type.specificity_type_dto import SpecificityTypeDto
from src.modules.domain.specificity.dto.specificity_type.specificity_type_query_dto import (
    FindAllSpecificityTypeQueryDto,
    OrderBySpecificityTypeQueryDto,
)
from src.modules.domain.specificity.dto.specificity_type.create_specificity_type_dto import CreateSpecificityTypeDto
from src.modules.domain.specificity.dto.specificity_type.update_specificity_type_dto import UpdateSpecificityTypeDto
from src.modules.domain.specificity.entities.specificity_type_entity import SpecificityType
from src.modules.domain.specificity.services.specificity_type_service import SpecificityTypeService
from src.modules.infrastructure.database import get_db

specificity_type_router = APIRouter(tags=["SpecificityType"], prefix="/specificity-type")

specificity_type_service = SpecificityTypeService()

@specificity_type_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=SpecificityTypeDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_specificity_type(
    request: CreateSpecificityTypeDto, database: Session = Depends(get_db)
) -> Optional[SpecificityTypeDto]:
    return await specificity_type_service.create_specificity_type(request, database)


@specificity_type_router.get(
    "/get/{id}",
    response_model=SpecificityTypeDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_specificity_type_by_id(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[SpecificityTypeDto]:
    return await specificity_type_service.find_one_specificity_type(str(id), database)


@specificity_type_router.delete(
    "/delete/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_specificity_type(
    id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await specificity_type_service.delete_specificity_type(str(id), database)


@specificity_type_router.patch(
    "/update/{id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_specificity_type(
    request: UpdateSpecificityTypeDto, id: UUID, database: Session = Depends(get_db)
) -> Optional[UpdateResult]:
    return await specificity_type_service.update_specificity_type(str(id), request, database)


@specificity_type_router.get(
    "/get",
    response_model=PaginationResponseDto[SpecificityTypeDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_specificity_type_paginated(
    pagination: FindManyOptions = Depends(
        GetPagination(
            SpecificityType,
            SpecificityTypeDto,
            FindAllSpecificityTypeQueryDto,
            OrderBySpecificityTypeQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[SpecificityTypeDto]]:
    return await specificity_type_service.get_all_specificity_type_paginated(pagination, database)
