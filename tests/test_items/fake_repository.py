from typing import Any

from bson import ObjectId

from src.items.schemas import ItemCreateSchema, ItemInMongo


class FakeItemRepository:
    def __init__(self) -> None:
        self.collection = {}

    async def add(self, item: ItemCreateSchema) -> ItemInMongo:
        id = ObjectId()
        new_item = item.model_dump()
        new_item.update({"id": id})
        self.collection[id] = new_item
        return ItemInMongo(**new_item)

    async def get(self, id: str) -> ItemInMongo | None:
        result = self.collection.get(id)
        if result is None:
            return None
        return ItemInMongo(**result)

    async def get_all(self, *args) -> list[ItemInMongo]:
        return [ItemInMongo(**item) for item in self.collection.values()]

    async def update(self, id: str, new_values: dict[str, Any]) -> ItemInMongo:
        self.collection[id].update(new_values)
        return ItemInMongo(**self.collection[id])

    async def delete(self, id: str) -> int:
        if id not in self.collection:
            return 0
        del self.collection[id]
        return 1
