from uuid import UUID

from pydantic import BaseModel, constr, Extra, Field


class CreateSpecificityDto(BaseModel):
    specificity_type_id: UUID = Field(alias="specificity_type")
    user_id: UUID = Field(alias="user")
    food_id: UUID = Field(alias="food")

    class Config:
        extra = Extra.forbid
