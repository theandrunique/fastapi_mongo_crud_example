from dataclasses import dataclass
from uuid import UUID

from src.repositories.base.items import ItemsRepository

from .schemas import ItemCreate, ItemSchema, ItemUpdate


@dataclass(kw_only=True)
class ItemsService:
    repository: ItemsRepository

    async def add(self, item_create: ItemCreate) -> ItemSchema:
        inserted_item = await self.repository.add(
            name=item_create.name, price=item_create.price, count=item_create.count
        )
        return inserted_item

    async def get_all(self, count: int, offset: int) -> list[ItemSchema]:
        result = await self.repository.get_many(count, offset)
        return result

    async def get(self, id: UUID) -> ItemSchema | None:
        result = await self.repository.get(id)
        if result:
            return result
        return None

    async def update(
        self,
        id: UUID,
        values: ItemUpdate,
    ) -> ItemSchema | None:
        item = await self.repository.get(id)
        if item is None:
            return None

        if values.count is not None:
            item.count = values.count

        if values.name is not None:
            item.name = values.name

        if values.price is not None:
            item.price = values.price

        await self.repository.update(id, item)
        return item

    async def delete(self, id: UUID) -> bool:
        item = await self.repository.get(id)
        if not item:
            return False

        return await self.repository.delete(id)
