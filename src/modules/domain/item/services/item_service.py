from typing import Optional

from sqlalchemy.orm import Session

from src.core.common.dto.pagination_response_dto import (
    create_pagination_response_dto,
    PaginationResponseDto,
)
from src.core.types.find_many_options_type import FindManyOptions
from src.core.types.update_result_type import UpdateResult
from src.modules.domain.item.dto.item.create_item_dto import CreateItemDto
from src.modules.domain.item.dto.item.item_dto import ItemDto
from src.modules.domain.item.dto.item.update_item_dto import UpdateItemDto
from src.modules.domain.item.entities.item_entity import Item
from src.modules.domain.item.interfaces.item_has_food_interface import ItemHasFoodInterface
from src.modules.domain.item.repositories.item_repository import ItemRepository
from src.modules.infrastructure.database.control_transaction import force_nested_transaction_forever


class ItemService:
    def __init__(self):
        self.item_repository = ItemRepository()
        self.item_has_food_interface = ItemHasFoodInterface()

    # ---------------------- PUBLIC METHODS ----------------------
    async def create_item(self, item_dto: CreateItemDto, db: Session) -> Optional[ItemDto]:
        try:
            with force_nested_transaction_forever(db):
                new_item = await self.item_repository.create(
                    Item(description=item_dto.description), db
                )
                new_item = await self.item_repository.save(new_item, db)

                new_item_foods = await self.item_has_food_interface.create_item_has_food(
                    new_item, item_dto.foods, db
                )

                response = ItemDto(**new_item.__dict__)
                response.foods = [new_item_food.food for new_item_food in new_item_foods]

            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e

    async def get_all_item_paginated(
        self, pagination: FindManyOptions, db: Session
    ) -> Optional[PaginationResponseDto[ItemDto]]:
        [all_item, total] = await self.item_repository.find_and_count(pagination, db)

        return create_pagination_response_dto(
            [ItemDto(**item.__dict__) for item in all_item],
            total,
            pagination["skip"],
            pagination["take"],
        )

    async def find_one_item(self, item_id: str, db: Session) -> Optional[ItemDto]:
        item = await self.item_repository.find_one_or_fail(
            {"where": Item.id == item_id, "relations": ["foods"]}, db
        )

        return ItemDto(**item.__dict__)

    async def delete_item(self, item_id: str, db: Session) -> Optional[UpdateResult]:
        return await self.item_repository.soft_delete(item_id, db)

    async def update_item(
        self, id: str, update_food_dto: UpdateItemDto, db: Session
    ) -> Optional[UpdateResult]:
        try:
            with force_nested_transaction_forever(db):
                list_foods = update_food_dto.foods
                del update_food_dto.foods

                response = await self.item_repository.update(id, update_food_dto, db)

                if list_foods:
                    response["affected"] += (
                        await self.item_has_food_interface.update_item_has_food(id, list_foods, db)
                    )["affected"]

            db.commit()
            return response
        except Exception as e:
            db.rollback()
            raise e
