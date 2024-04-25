from typing import Any

from motor.motor_asyncio import AsyncIOMotorClientSession
from pymongo import ReturnDocument

from src.mongo import PyObjectId, db

from .schemas import Item, ItemCreate

item_collection = db["items"]


class ItemRepository:
    def __init__(self, session: AsyncIOMotorClientSession) -> None:
        self.session = session

    async def add(self, item: ItemCreate) -> Item:
        result = await item_collection.insert_one(
            item.model_dump(),
            session=self.session,
        )
        new_item = Item(
            id=result.inserted_id,
            **item.model_dump(),
        )
        return new_item

    async def get_all(self, count: int, offset: int) -> list[Item]:
        result = (
            await item_collection.find(session=self.session)
            .skip(offset)
            .to_list(length=count)
        )
        return [Item(**item) for item in result]

    async def get(self, id: PyObjectId) -> Item | None:
        result = await item_collection.find_one({"_id": id}, session=self.session)
        if result is None:
            return None
        return Item(**result)

    async def update(self, id: PyObjectId, new_values: dict[str, Any]) -> Item:
        updated_app = await item_collection.find_one_and_update(
            {"_id": id},
            {"$set": new_values},
            return_document=ReturnDocument.AFTER,
            session=self.session,
        )
        return Item(**updated_app)

    async def delete(self, id: PyObjectId) -> int:
        result = await item_collection.delete_one({"_id": id}, session=self.session)
        return result.deleted_count
