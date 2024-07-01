from dataclasses import dataclass
from uuid import UUID

from src.items.dto import ItemDTO
from src.repositories.base.items import ItemsRepository

from .schemas import ItemCreate, ItemUpdate
from .service_exc import (
    DeleteItemError,
)


@dataclass(kw_only=True)
class ItemsService:
    repository: ItemsRepository

    async def add(self, item_create: ItemCreate) -> ItemDTO:
        inserted_item = await self.repository.add(
            name=item_create.name,
            price=item_create.price,
            count=item_create.count,
        )
        return inserted_item

    async def get_all(self, count: int, offset: int) -> tuple[list[ItemDTO], int]:
        result = await self.repository.get_many(count, offset)
        count = await self.repository.count()
        return result, count

    async def get(self, id: UUID) -> ItemDTO | None:
        result = await self.repository.get(id)
        if result:
            return result
        return None

    async def update(
        self,
        id: UUID,
        values: ItemUpdate,
    ) -> None:
        updated_item = ItemDTO(
            id=id,
            name=values.name,
            price=values.price,
            count=values.count,
        )

        await self.repository.update(id, updated_item)

    async def delete(self, id: UUID) -> None:
        item = await self.repository.get(id)
        if not item:
            raise DeleteItemError(f"Item with ID {id} was not found for deletion")

        await self.repository.delete(id)
