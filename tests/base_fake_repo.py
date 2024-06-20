from typing import Any

from bson import ObjectId


class BaseFakeRepository[T]:
    def __init__(self) -> None:
        self.collection: dict[T, dict[str, Any]] = {}

    async def add(self, item: dict[str, Any]) -> T:
        if "id" not in item:
            id = ObjectId()
        else:
            id = item["id"]
        item.update({"id": id})
        self.collection[id] = item  # pyright: ignore
        return id

    async def get(self, id: T) -> dict[str, Any] | None:
        return self.collection.get(id)

    async def get_many(self, *args) -> list[dict[str, Any]]:
        return list(self.collection.values())

    async def update(self, id: T, new_values: dict[str, Any]):
        self.collection[id].update(new_values)
        return self.collection[id]

    async def delete(self, id: T) -> int:
        if id not in self.collection:
            return 0
        del self.collection[id]
        return 1
