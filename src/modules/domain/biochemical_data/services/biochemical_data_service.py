import os
import uuid
from copy import deepcopy
from datetime import date
from typing import Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.biochemical_data.dto.biochemical_data_dto import BiochemicalDataDto
from src.modules.domain.biochemical_data.dto.create_biochemical_data_dto import (
    CreateBiochemicalDataDto,
)
from src.modules.domain.biochemical_data.dto.update_biochemical_data_dto import (
    UpdateBiochemicalDataDto,
)
from src.modules.domain.biochemical_data.entities.biochemical_data_entity import (
    BiochemicalData,
)
from src.modules.domain.biochemical_data.repositories.biochemical_data_repository import (
    BiochemicalDataRepository,
)


class BiochemicalDataService:
    def __init__(self):
        self.biochemical_data_repository = BiochemicalDataRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_biochemical_data(
        self, biochemical_data_dto: CreateBiochemicalDataDto, db: Session
    ) -> Optional[BiochemicalDataDto]:
        new_biochemical_data = await self.biochemical_data_repository.create(biochemical_data_dto, db)

        new_biochemical_data = self.biochemical_data_repository.save(new_biochemical_data, db)
        return BiochemicalDataDto(**new_biochemical_data.__dict__)

    async def get_all_biochemical_data(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[BiochemicalDataDto]]:
        [
            all_biochemical_data,
            total,
        ] = await self.biochemical_data_repository.find_and_count(
            pagination,
            db,
        )

        return create_pagination_response_dto(
            [BiochemicalDataDto(**biochemical_data.__dict__) for biochemical_data in all_biochemical_data],
            total,
            pagination["skip"],
            pagination["take"],
        )
    
    async def get_biochemical_data_by_id(
        self, biochemical_data_id: str, db: Session
    ) -> Optional[BiochemicalDataDto]:
        biochemical_data = await self.biochemical_data_repository.find_one_or_fail(
            {
                "where": BiochemicalData.id == biochemical_data_id,
                "relations": ["appointment"],
            },
            db,
        )

        return BiochemicalDataDto(**biochemical_data.__dict__)

    async def update_biochemical_data(
        self,
        biochemical_data_id: str,
        update_biochemical_data_dto: Union[
            UpdateBiochemicalDataDto
        ],
        db: Session,
    ) -> Optional[UpdateResult]:
        update_biochemical_data_dto = self.__verify_values(update_biochemical_data_dto)

        try:
            with db.begin_nested():

                if isinstance(update_biochemical_data_dto, UpdateBiochemicalDataDto):
                    if "body_photo" in update_biochemical_data_dto.dict(exclude_unset=True):
                        image = self.image_utils.valid_image64(
                            update_biochemical_data_dto.body_photo
                        )
                    delattr(update_biochemical_data_dto, "body_photo")

                    biochemical_data = (
                        await self.biochemical_data_repository.find_one_or_fail(
                            biochemical_data_id, db
                        )
                    )
                    if "image" in locals():
                        if image:
                            biochemical_data.body_photo = self.image_utils.save_image(
                                str(biochemical_data.id), image
                            )
                            update_biochemical_data_dto.body_photo = (
                                f"{biochemical_data.id}.{image['format']}"
                            )
                        else:
                            self.image_utils.delete_image(str(biochemical_data.body_photo))
                            update_biochemical_data_dto.body_photo = None

            return await self.biochemical_data_repository.update(
                biochemical_data_id, update_biochemical_data_dto, db
            )
        except Exception as e:
            db.rollback()
            raise e

    async def delete_biochemical_data(
        self, biochemical_data_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.biochemical_data_repository.soft_delete(biochemical_data_id, db)

    # ---------------------- PRIVATE METHODS ----------------------
    @staticmethod
    def __verify_values(
        biochemical_data_dto: Union[CreateBiochemicalDataDto, UpdateBiochemicalDataDto],
    ) -> Union[CreateBiochemicalDataDto, UpdateBiochemicalDataDto]:
        for key in [
            "total_proteins",
            "albumin",
            "urea",
            "uric_acid",
            "creatinine",
            "total_cholesterol",
            "hdl",
            "ldl",
            "glycemia",
            "hda1c",
            "fasting_glycemia",
            "post_prandial_glycemia",
            "total_bilirubin",
            "biliburin_direct",
            "alkaline_phosphatase",
            "ast_tgo",
            "alt_tgp",
            "ygt"
        ]:
            if (
                key in biochemical_data_dto.__dict__
                and biochemical_data_dto.__dict__[key] is not None
                and biochemical_data_dto.__dict__[key] < 0
            ):
                raise BadRequestException(f"{key} must be greater than or equal to 0")

        return biochemical_data_dto
