from dataclasses import dataclass
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import ReturnDocument

from src.mongo import PyObjectId
from src.mongo.base_repository import BaseMongoRepository


@dataclass(kw_only=True)
class ItemsRepository(BaseMongoRepository):
    collection: AsyncIOMotorCollection

    async def add(self, item: dict[str, Any]) -> Any:
        result = await self.collection.insert_one(item)
        return result.inserted_id

    async def get_many(self, count: int, offset: int) -> list[dict[str, Any]]:
        result = await self.collection.find().skip(offset).to_list(length=count)
        return result

    async def get(self, id: PyObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": id})

    async def update(
        self,
        id: PyObjectId,
        new_values: dict[str, Any],
    ) -> dict[str, Any]:
        updated: dict[str, Any] = await self.collection.find_one_and_update(
            {"_id": id},
            {"$set": new_values},
            return_document=ReturnDocument.AFTER,
        )
        return updated

    async def delete(self, id: PyObjectId) -> int:
        result = await self.collection.delete_one({"_id": id})
        return result.deleted_count
