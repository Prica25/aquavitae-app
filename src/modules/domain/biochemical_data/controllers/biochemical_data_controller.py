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
from src.modules.domain.biochemical_data.dto.biochemical_data_dto import BiochemicalDataDto
from src.modules.domain.biochemical_data.dto.biochemical_data_query_dto import (
    FindAllBiochemicalDataQueryDto,
    OrderByBiochemicalDataQueryDto,
)
from src.modules.domain.biochemical_data.dto.create_biochemical_data_dto import (
    CreateBiochemicalDataDto,
)
from src.modules.domain.biochemical_data.dto.update_biochemical_data_dto import (
    UpdateBiochemicalDataDto,
)
from src.modules.domain.biochemical_data.entities.biochemical_data_entity import (
    BiochemicalData,
)
from src.modules.domain.biochemical_data.services.biochemical_data_service import (
    BiochemicalDataService,
)
from src.modules.infrastructure.auth.auth_controller import get_current_user
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.entities.user_entity import User

biochemical_data_router = APIRouter(tags=["Biochemical Data"], prefix="/biochemical-data")

biochemical_data_service = BiochemicalDataService()


@biochemical_data_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=BiochemicalDataDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_biochemical_data(
    request: CreateBiochemicalDataDto, database: Session = Depends(get_db)
) -> Optional[BiochemicalDataDto]:
    return await biochemical_data_service.create_biochemical_data(request, database)


@biochemical_data_router.get(
    "/get",
    response_model=PaginationResponseDto[BiochemicalDataDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_biochemical_data(
    pagination: FindManyOptions = Depends(
        GetPagination(
            BiochemicalData,
            BiochemicalDataDto,
            FindAllBiochemicalDataQueryDto,
            OrderByBiochemicalDataQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[BiochemicalDataDto]]:
    return await biochemical_data_service.get_all_biochemical_data(pagination, database)


@biochemical_data_router.get(
    "/get/{biochemical_data_id}",
    response_model=BiochemicalDataDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_biochemical_data_by_id(
    biochemical_data_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[BiochemicalDataDto]:
    return await biochemical_data_service.get_biochemical_data_by_id(
        str(biochemical_data_id), database
    )


@biochemical_data_router.patch(
    "/update/{biochemical_data_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_biochemical_data(
    biochemical_data_id: UUID,
    request: UpdateBiochemicalDataDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await biochemical_data_service.update_biochemical_data(
        str(biochemical_data_id), request, database
    )


@biochemical_data_router.delete(
    "/delete/{biochemical_data_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_biochemical_data(
    biochemical_data_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await biochemical_data_service.delete_biochemical_data(
        str(biochemical_data_id), database
    )
