from typing import Any

from pymongo import ReturnDocument

from src.mongo import db

from .schemas import ItemCreateSchema, ItemInMongo

item_collection = db["items"]


class ItemRepository:
    def __init__(self) -> None: ...

    async def add(self, item: ItemCreateSchema) -> ItemInMongo:
        result = await item_collection.insert_one(
            item.model_dump(),
        )
        new_item = ItemInMongo(
            id=result.inserted_id,
            **item.model_dump(),
        )
        return new_item

    async def get_all(self, count: int, offset: int) -> list[ItemInMongo]:
        result = await item_collection.find().skip(offset).to_list(length=count)
        return [ItemInMongo(**item) for item in result]

    async def get(self, id: str) -> ItemInMongo | None:
        result = await item_collection.find_one({"_id": id})
        if result is None:
            return None
        return ItemInMongo(**result)

    async def update(self, id: str, new_values: dict[str, Any]) -> ItemInMongo:
        updated_app = await item_collection.find_one_and_update(
            {"_id": id},
            {"$set": new_values},
            return_document=ReturnDocument.AFTER,
        )
        return ItemInMongo(**updated_app)

    async def delete(self, id: str) -> int:
        result = await item_collection.delete_one({"_id": id})
        return result.deleted_count
