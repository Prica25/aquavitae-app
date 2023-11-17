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
from src.modules.domain.diagnosis.dto.diagnosis_dto import DiagnosisDto
from src.modules.domain.diagnosis.dto.diagnosis_query_dto import (
    FindAllDiagnosisQueryDto,
    OrderByDiagnosisQueryDto,
)
from src.modules.domain.diagnosis.dto.create_diagnosis_dto import (
    CreateDiagnosisDto,
)
from src.modules.domain.diagnosis.dto.update_diagnosis_dto import (
    UpdateDiagnosisDto,
)
from src.modules.domain.diagnosis.entities.diagnosis_entity import (
    Diagnosis,
)
from src.modules.domain.diagnosis.services.diagnosis_service import (
    DiagnosisService,
)
from src.modules.infrastructure.database import get_db
from src.modules.infrastructure.user.entities.user_entity import User

diagnosis_router = APIRouter(tags=["Diagnosis"], prefix="/diagnosis")

diagnosis_service = DiagnosisService()


@diagnosis_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=DiagnosisDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_diagnosis(
    request: CreateDiagnosisDto, database: Session = Depends(get_db)
) -> Optional[DiagnosisDto]:
    return await diagnosis_service.create_diagnosis(request, database)


@diagnosis_router.get(
    "/get",
    response_model=PaginationResponseDto[DiagnosisDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_diagnosis(
    pagination: FindManyOptions = Depends(
        GetPagination(
            Diagnosis,
            DiagnosisDto,
            FindAllDiagnosisQueryDto,
            OrderByDiagnosisQueryDto,
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[DiagnosisDto]]:
    return await diagnosis_service.get_all_diagnosis(pagination, database)


@diagnosis_router.get(
    "/get/{diagnosis_id}",
    response_model=DiagnosisDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_diagnosis_by_id(
    diagnosis_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[DiagnosisDto]:
    return await diagnosis_service.get_diagnosis_by_id(
        str(diagnosis_id), database
    )


@diagnosis_router.patch(
    "/update/{diagnosis_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_diagnosis(
    diagnosis_id: UUID,
    request: UpdateDiagnosisDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await diagnosis_service.update_diagnosis(
        str(diagnosis_id), request, database
    )


@diagnosis_router.delete(
    "/delete/{diagnosis_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_diagnosis(
    diagnosis_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await diagnosis_service.delete_diagnosis(
        str(diagnosis_id), database
    )
