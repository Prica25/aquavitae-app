from typing import Optional, Union

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.exceptions_type import BadRequestException
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.diagnosis.dto.diagnosis_dto import DiagnosisDto
from src.modules.domain.diagnosis.dto.create_diagnosis_dto import (
    CreateDiagnosisDto,
)
from src.modules.domain.diagnosis.dto.update_diagnosis_dto import (
    UpdateDiagnosisDto,
)
from src.modules.domain.diagnosis.entities.diagnosis_entity import (
    Diagnosis,
)
from src.modules.domain.diagnosis.repositories.diagnosis_repository import (
    DiagnosisRepository,
)


class DiagnosisService:
    def __init__(self):
        self.diagnosis_repository = DiagnosisRepository()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_diagnosis(
        self, diagnosis_dto: CreateDiagnosisDto, db: Session
    ) -> Optional[DiagnosisDto]:
        try:
            new_diagnosis = await self.diagnosis_repository.create(diagnosis_dto, db)
            new_diagnosis = self.diagnosis_repository.save(new_diagnosis, db)
            return DiagnosisDto.from_orm(new_diagnosis)
        except Exception as e:
            db.rollback()
            raise e

    async def get_all_diagnosis(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[DiagnosisDto]]:
        [
            all_user_diagnosis,
            total,
        ] = await self.diagnosis_repository.find_and_count(
            pagination,
            db,
        )

        all_diagnosis_dto = []
        for diagnosis in all_user_diagnosis:
            all_diagnosis_dto.append(
                DiagnosisDto(**diagnosis.__dict__)
            )

        return create_pagination_response_dto(
            all_diagnosis_dto,
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def get_diagnosis_by_id(
        self, diagnosis_id: str, db: Session
    ) -> Optional[DiagnosisDto]:
        diagnosis = await self.diagnosis_repository.find_one_or_fail(
            {
                "where": Diagnosis.id == diagnosis_id,
                "relations": ["user"],
            },
            db,
        )

        return DiagnosisDto(**diagnosis.__dict__)

    async def update_diagnosis(
        self,
        diagnosis_id: str,
        update_diagnosis_dto: Union[
            UpdateDiagnosisDto
        ],
        db: Session,
    ) -> Optional[UpdateResult]:
        try:
            with db.begin_nested():

                if isinstance(update_diagnosis_dto, UpdateDiagnosisDto):
                    if "body_photo" in update_diagnosis_dto.dict(exclude_unset=True):
                        image = self.image_utils.valid_image64(
                            update_diagnosis_dto.body_photo
                        )
                    delattr(update_diagnosis_dto, "body_photo")

                    diagnosis = (
                        await self.diagnosis_repository.find_one_or_fail(
                            diagnosis_id, db
                        )
                    )
                    if "image" in locals():
                        if image:
                            diagnosis.body_photo = self.image_utils.save_image(
                                str(diagnosis.id), image
                            )
                            update_diagnosis_dto.body_photo = (
                                f"{diagnosis.id}.{image['format']}"
                            )
                        else:
                            self.image_utils.delete_image(str(diagnosis.body_photo))
                            update_diagnosis_dto.body_photo = None

            return await self.diagnosis_repository.update(
                diagnosis_id, update_diagnosis_dto, db
            )
        except Exception as e:
            db.rollback()
            raise e

    async def delete_diagnosis(
        self, diagnosis_id: str, db: Session
    ) -> Optional[UpdateResult]:
        return await self.diagnosis_repository.soft_delete(diagnosis_id, db)

    # ---------------------- PRIVATE METHODS ----------------------