from dataclasses import dataclass, field

from beanie import Document
from pydantic import BaseModel


@dataclass
class MongoDBRepository[ModelType: Document, SchemaType: BaseModel, IDType]:
    model: type[ModelType] = field(init=False)
    schema: type[SchemaType] = field(init=False)

    async def add(self, **kwargs) -> SchemaType:
        new_item = self.model(**kwargs)
        await new_item.insert()
        return self.schema.model_validate(new_item, from_attributes=True)

    async def get(self, id: IDType) -> SchemaType | None:
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def get_many(
        self, count: int, offset: int, **filters
    ) -> tuple[list[SchemaType], int]:
        query = self.model.find_many(sort=list(filters.items()))
        items = await query.skip(offset).to_list(count)
        return [
            self.schema.model_validate(item, from_attributes=True) for item in items
        ], await query.count()

    async def update(self, id: IDType, updated_item: SchemaType):
        updated_item_model = self.model(id=id, **updated_item.model_dump())
        await updated_item_model.replace()

    async def delete(self, id: IDType) -> bool:
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return False
        await item.delete()
        return True
