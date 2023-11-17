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
from src.modules.domain.plan_meals.dto.meals_of_plan.meals_of_plan_dto import MealsOfPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.meals_of_plan_query_dto import (
    FindAllMealsOfPlanQueryDto,
    OrderByMealsOfPlanQueryDto,
)
from src.modules.domain.plan_meals.dto.meals_of_plan.create_meals_of_plan_dto import CreateMealsOfPlanDto
from src.modules.domain.plan_meals.dto.meals_of_plan.update_meals_of_plan_dto import UpdateMealsOfPlanDto

from src.modules.domain.plan_meals.entities.meals_of_plan_entity import MealsOfPlan
from src.modules.domain.plan_meals.services.meals_of_plan_service import MealsOfPlanService
from src.modules.infrastructure.database import get_db

meals_of_plan_router = APIRouter(tags=["Meals of Plan"], prefix="/meals-of-plan")

meals_of_plan_service = MealsOfPlanService()


@meals_of_plan_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=MealsOfPlanDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_meals_of_plan_goal(
    request: CreateMealsOfPlanDto, database: Session = Depends(get_db)
) -> Optional[MealsOfPlanDto]:
    return await meals_of_plan_service.create_meals_of_plan(request, database)


@meals_of_plan_router.get(
    "/get",
    response_model=PaginationResponseDto[MealsOfPlanDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_meals_of_plans(
    pagination: FindManyOptions = Depends(
        GetPagination(
            MealsOfPlan, MealsOfPlanDto, FindAllMealsOfPlanQueryDto, OrderByMealsOfPlanQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[MealsOfPlanDto]]:
    return await meals_of_plan_service.get_all_meals_of_plans(pagination, database)


@meals_of_plan_router.get(
    "/get/{meals_of_plan_id}",
    response_model=MealsOfPlanDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_meals_of_plan_by_id(
    meals_of_plan_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[MealsOfPlanDto]:
    return await meals_of_plan_service.get_meals_of_plan_by_id(str(meals_of_plan_id), database)


@meals_of_plan_router.patch(
    "/update/{meals_of_plan_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_meals_of_plan(
    meals_of_plan_id: UUID,
    request: UpdateMealsOfPlanDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await meals_of_plan_service.update_meals_of_plan(str(meals_of_plan_id), request, database)


@meals_of_plan_router.delete(
    "/delete/{meals_of_plan_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_meals_of_plan(
    meals_of_plan_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await meals_of_plan_service.delete_meals_of_plan(str(meals_of_plan_id), database)
