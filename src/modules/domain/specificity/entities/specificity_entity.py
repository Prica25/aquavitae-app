from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.modules.infrastructure.database.base_entity import BaseEntity


@dataclass
class Specificity(BaseEntity):
    specificity_type_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("specificity_type.id", ondelete="CASCADE"), nullable=False
    )
    specificity_type = relationship("SpecificityType", back_populates="specificities")

    food_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("food.id", ondelete="CASCADE"), nullable=False
    )
    food = relationship("Food", back_populates="specificities")

    user_id: UUID = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="specificities")

    def __init__(
        self, specificity_type_id: UUID, user_id: UUID, food_id: UUID, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.specificity_type_id = specificity_type_id
        self.user_id = user_id
        self.food_id = food_id
