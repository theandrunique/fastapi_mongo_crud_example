from typing import Any

from pymongo import ReturnDocument

from src.mongo import PyObjectId, db

from .schemas import Item, ItemCreate

item_collection = db["items"]


class ItemRepository:
    def __init__(self) -> None: ...

    async def add(self, item: ItemCreate) -> Item:
        result = await item_collection.insert_one(
            item.model_dump(),
        )
        new_item = Item(
            id=result.inserted_id,
            **item.model_dump(),
        )
        return new_item

    async def get_all(self, count: int, offset: int) -> list[Item]:
        result = await item_collection.find().skip(offset).to_list(length=count)
        return [Item(**item) for item in result]

    async def get(self, id: PyObjectId) -> Item | None:
        result = await item_collection.find_one({"_id": id})
        if result is None:
            return None
        return Item(**result)

    async def update(self, id: PyObjectId, new_values: dict[str, Any]) -> Item:
        updated_app = await item_collection.find_one_and_update(
            {"_id": id},
            {"$set": new_values},
            return_document=ReturnDocument.AFTER,
        )
        return Item(**updated_app)

    async def delete(self, id: PyObjectId) -> int:
        result = await item_collection.delete_one({"_id": id})
        return result.deleted_count
