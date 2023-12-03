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
from src.modules.domain.plan_meals.dto.meals_options.meals_options_dto import MealsOptionsDto
from src.modules.domain.plan_meals.dto.meals_options.meals_options_query_dto import (
    FindAllMealsOptionsQueryDto,
    OrderByMealsOptionsQueryDto,
)
from src.modules.domain.plan_meals.dto.meals_options.create_meals_options_dto import CreateMealsOptionsDto
from src.modules.domain.plan_meals.dto.meals_options.update_meals_options_dto import UpdateMealsOptionsDto

from src.modules.domain.plan_meals.entities.meals_options_entity import MealsOptions
from src.modules.domain.plan_meals.services.meals_options_service import MealsOptionsService
from src.modules.infrastructure.database import get_db

meals_options_router = APIRouter(tags=["Meals Options"], prefix="/meals-options")

meals_options_service = MealsOptionsService()


@meals_options_router.post(
    "/create",
    status_code=HTTP_201_CREATED,
    response_model=MealsOptionsDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def create_meals_options(
    request: CreateMealsOptionsDto, database: Session = Depends(get_db)
) -> Optional[MealsOptionsDto]:
    return await meals_options_service.create_meals_options(request, database)


@meals_options_router.get(
    "/get",
    response_model=PaginationResponseDto[MealsOptionsDto],
    response_model_exclude_unset=True,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_all_meals_optionss(
    pagination: FindManyOptions = Depends(
        GetPagination(
            MealsOptions, MealsOptionsDto, FindAllMealsOptionsQueryDto, OrderByMealsOptionsQueryDto
        )
    ),
    database: Session = Depends(get_db),
) -> Optional[PaginationResponseDto[MealsOptionsDto]]:
    return await meals_options_service.get_all_meals_optionss(pagination, database)


@meals_options_router.get(
    "/get/{meals_options_id}",
    response_model=MealsOptionsDto,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def get_meals_options_by_id(
    meals_options_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[MealsOptionsDto]:
    return await meals_options_service.get_meals_options_by_id(str(meals_options_id), database)


@meals_options_router.patch(
    "/update/{meals_options_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def update_meals_options(
    meals_options_id: UUID,
    request: UpdateMealsOptionsDto,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await meals_options_service.update_meals_options(str(meals_options_id), request, database)


@meals_options_router.delete(
    "/delete/{meals_options_id}",
    response_model=UpdateResult,
    dependencies=[Depends(Auth([UserRole.ADMIN, UserRole.NUTRITIONIST]))],
)
async def delete_meals_options(
    meals_options_id: UUID,
    database: Session = Depends(get_db),
) -> Optional[UpdateResult]:
    return await meals_options_service.delete_meals_options(str(meals_options_id), database)

