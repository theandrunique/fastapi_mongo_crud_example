from dataclasses import dataclass
from typing import Any

from src.mongo.base_repository import BaseMongoRepository
from src.mongo.object_id import PyObjectId

from .schemas import Item, ItemCreate, ItemUpdate


@dataclass(kw_only=True)
class ItemsService:
    repository: BaseMongoRepository

    async def add(self, item: ItemCreate) -> Any:
        return await self.repository.add(item.model_dump())

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
    ) -> dict[str, Any] | None:
        new_values = values.model_dump(exclude_defaults=True)
        if new_values:
            return await self.repository.update(id, new_values)
        return None


    async def delete(self, id: PyObjectId) -> int:
        return await self.repository.delete(id)

