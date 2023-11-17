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
from src.modules.domain.nutritional_plan.dto.nutritional_plan_dto import NutritionalPlanDto
from src.modules.domain.nutritional_plan.dto.nutritional_plan_query_dto import (
    FindAllNutritionalPlanQueryDto,
    OrderByNutritionalPlanQueryDto,
)
from src.modules.domain.nutritional_plan.dto.create_nutritional_plan_dto import (
    CreateNutritionalPlanDto,
)
from src.modules.domain.nutritional_plan.dto.update_nutritional_plan_dto import (
    UpdateNutritionalPlanDto,
)
from src.modules.domain.nutritional_plan.entities.nutritional_plan_entity import NutritionalPlan
from src.modules.domain.nutritional_plan.services.nutritional_plan_service import NutritionalPlanService
from src.modules.infrastructure.database import get_db

nutritional_plan_router = APIRouter(tags=["Nutritional Plan"], prefix="/nutritional-plan")

nutritional_plan_service = NutritionalPlanService()


@nutritional_plan_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=NutritionalPlanDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_nutritional_plan_goal(
    request: CreateNutritionalPlanDto, database: Session = Depends(get_db)
) -> Optional[NutritionalPlanDto]:
    return await nutritional_plan_service.create_nutritional_plan(request, database)


@nutritional_plan_router.get(
    "/get",
    response_model=PaginationResponseDto[NutritionalPlanDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_nutritional_plans(
    pagination: FindManyOptions = Depends(
        GetPagination(
            NutritionalPlan, NutritionalPlanDto, FindAllNutritionalPlanQueryDto, OrderByNutritionalPlanQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[NutritionalPlanDto]]:
    return await nutritional_plan_service.get_all_nutritional_plans(pagination, database)


@nutritional_plan_router.get(
    "/get/{nutritional_plan_id}",
    response_model=NutritionalPlanDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_nutritional_plan_by_id(
    nutritional_plan_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[NutritionalPlanDto]:
    return await nutritional_plan_service.get_nutritional_plan_by_id(str(nutritional_plan_id), database)


@nutritional_plan_router.patch(
    "/update/{nutritional_plan_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_nutritional_plan(
    nutritional_plan_id: UUID,
    request: UpdateNutritionalPlanDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await nutritional_plan_service.update_nutritional_plan(str(nutritional_plan_id), request, database)


@nutritional_plan_router.delete(
    "/delete/{nutritional_plan_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_nutritional_plan(
    nutritional_plan_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await nutritional_plan_service.delete_nutritional_plan(str(nutritional_plan_id), database)
