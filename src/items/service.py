from dataclasses import dataclass
from uuid import UUID

from src.items.exceptions import ItemNotFound
from src.repositories.base.items import ItemsRepository

from .schemas import ItemCreate, ItemSchema, ItemUpdate


@dataclass(kw_only=True)
class ItemsService:
    repository: ItemsRepository

    async def add(self, item_create: ItemCreate) -> ItemSchema:
        inserted_item = await self.repository.add(
            name=item_create.name,
            price=item_create.price,
            count=item_create.count,
        )
        return inserted_item

    async def get_all(self, count: int, offset: int) -> tuple[list[ItemSchema], int]:
        result = await self.repository.get_many(count, offset)
        count = await self.repository.count()
        return result, count

    async def get(self, id: UUID) -> ItemSchema | None:
        result = await self.repository.get(id)
        if result:
            return result
        return None

    async def update(
        self,
        id: UUID,
        values: ItemUpdate,
    ) -> None:
        item = await self.repository.get(id)
        if item is None:
            raise ItemNotFound()

        if values.count is not None:
            item.count = values.count

        if values.name is not None:
            item.name = values.name

        if values.price is not None:
            item.price = values.price

        await self.repository.update(id, item)

    async def delete(self, id: UUID) -> None:
        item = await self.repository.get(id)
        if not item:
            raise ItemNotFound()

        await self.repository.delete(id)
