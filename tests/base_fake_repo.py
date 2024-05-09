from typing import Any

from bson import ObjectId

from src.mongo.base_repository import BaseMongoRepository


class BaseFakeRepository(BaseMongoRepository):
    def __init__(self) -> None:
        self.collection: dict[ObjectId, dict[str, Any]] = {}

    async def add(self, item: dict[str, Any]):
        id = ObjectId()
        item.update({"id": id})
        self.collection[id] = item
        return id

    async def get(self, id: Any):
        return self.collection.get(id)

    async def get_many(self, *args) -> list[dict[str, Any]]:
        return list(self.collection.values())

    async def update(self, id: Any, new_values: dict[str, Any]):
        self.collection[id].update(new_values)
        return self.collection[id]

    async def delete(self, id: Any) -> int:
        if id not in self.collection:
            return 0
        del self.collection[id]
        return 1
