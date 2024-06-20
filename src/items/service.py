from dataclasses import dataclass

from src.repositories.base.items import ItemsRepository
from src.schemas import PyObjectId

from .schemas import Item, ItemCreate, ItemUpdate


@dataclass(kw_only=True)
class ItemsService:
    repository: ItemsRepository

    async def add(self, item_create: ItemCreate) -> Item:
        inserted_id = await self.repository.add(item_create.model_dump())

        inserted_item = await self.repository.get(inserted_id)
        assert inserted_item is not None, "Item not found after insert"
        return Item(**inserted_item)

    async def get_all(self, count: int, offset: int) -> list[Item]:
        result = await self.repository.get_many(count, offset)
        return [Item(**item) for item in result]

    async def get(self, id: PyObjectId) -> Item | None:
        result = await self.repository.get(id)
        if result:
            return Item(**result)
        return None

    async def update(
        self,
        id: PyObjectId,
        values: ItemUpdate,
    ) -> Item | None:
        new_values = values.model_dump(exclude_defaults=True)
        if new_values:
            updated_item = await self.repository.update(id, new_values)
            return Item(**updated_item)
        return None

    async def delete(self, id: PyObjectId) -> int:
        return await self.repository.delete(id)
