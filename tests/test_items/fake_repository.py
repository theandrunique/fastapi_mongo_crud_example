from typing import Any

from bson import ObjectId

from src.items.schemas import Item, ItemCreate


class FakeItemRepository:
    def __init__(self) -> None:
        self.collection = {}

    async def add(self, item: ItemCreate) -> Item:
        id = ObjectId()
        new_item = item.model_dump()
        new_item.update({"id": id})
        self.collection[id] = new_item
        return Item(**new_item)

    async def get(self, id: str) -> Item | None:
        result = self.collection.get(id)
        if result is None:
            return None
        return Item(**result)

    async def get_all(self, *args) -> list[Item]:
        return [Item(**item) for item in self.collection.values()]

    async def update(self, id: str, new_values: dict[str, Any]) -> Item:
        self.collection[id].update(new_values)
        return Item(**self.collection[id])

    async def delete(self, id: str) -> int:
        if id not in self.collection:
            return 0
        del self.collection[id]
        return 1
