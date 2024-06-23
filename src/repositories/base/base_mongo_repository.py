from abc import ABC
from dataclasses import dataclass

from beanie import Document
from pydantic import BaseModel


@dataclass
class BaseMongoDBRepository[ModelType: Document, SchemaType: BaseModel, IDType](ABC):
    model: type[ModelType]
    schema: type[SchemaType]

    async def add(self, **kwargs) -> SchemaType:
        new_item = self.model(**kwargs)
        await new_item.insert()
        return self.schema.model_validate(new_item, from_attributes=True)

    async def get(self, id: IDType) -> SchemaType | None:
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def get_many(self, count: int, offset: int) -> list[SchemaType]:
        items = await self.model.find_many().skip(offset).to_list(length=count)
        return [
            self.schema.model_validate(item, from_attributes=True) for item in items
        ]

    async def update(self, id: IDType, updated_item: SchemaType):
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return None
        await item.set(updated_item.model_dump())

    async def delete(self, id: IDType) -> bool:
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return False
        await item.delete()
        return True
