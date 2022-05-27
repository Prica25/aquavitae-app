from typing import TypedDict

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.modules.infrastructure.database.base_entity import BaseEntity


class BaseOptionsDto(TypedDict):
    excludeFields: bool


class BaseDto:
    id: UUID
    created_at: DateTime
    updated_at: DateTime
    deleted_at: DateTime

    def __init__(self, entity: BaseEntity, options: BaseOptionsDto = None):
        if not options or not options['excludeFields']:
            self.id = entity.id
            self.created_at = entity.created_at
            self.updated_at = entity.updated_at
            self.deleted_at = entity.deleted_at
