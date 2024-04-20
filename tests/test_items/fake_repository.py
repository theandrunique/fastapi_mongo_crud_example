from typing import Any

from bson import ObjectId

from src.items.schemas import ItemCreateSchema, ItemInMongo


class FakeItemRepository:
    def __init__(self) -> None:
        self.collection = {}

    async def add(self, item: ItemCreateSchema) -> ItemInMongo:
        id = ObjectId()
        self.collection[id] = item.model_dump().update({"id": id})
        return self.collection[id]

    async def get(self, id: str) -> ItemInMongo | None:
        result = await self.collection.get(id)
        if result is None:
            return None
        return ItemInMongo(**result)

    async def update(self, id: str, new_values: dict[str, Any]) -> ItemInMongo:
        self.collection[id].update(new_values)
        return ItemInMongo(self.collection[id])

    async def delete(self, id: str) -> int:
        if id not in self.collection:
            return 0
        del self.collection[id]
        return 1

