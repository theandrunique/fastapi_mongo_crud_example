from dataclasses import asdict, dataclass, field

from beanie import Document

from src.dto import BaseDTO
from src.repositories.base.repository import Repository


@dataclass
class MongoDBRepository[Model: Document, DTO: BaseDTO, ID](Repository):
    model: type[Model] = field(init=False)
    schema: type[DTO] = field(init=False)

    async def add(self, **kwargs) -> DTO:
        new_item = self.model(**kwargs)
        await new_item.insert()
        return self.schema.from_orm(new_item)

    async def get(self, id: ID) -> DTO | None:
        item = await self.model.find_one(self.model.id == id)
        if item is None:
            return None
        return self.schema.from_orm(item)

    async def get_many(
        self,
        count: int,
        offset: int,
    ) -> list[DTO]:
        query = self.model.find_many()
        items = await query.skip(offset).to_list(count)
        return [self.schema.from_orm(item) for item in items]

    async def count(self) -> int:
        return await self.model.count()

    async def update(self, id: ID, updated_item: DTO):
        updated_item_model = self.model(id=id, **asdict(updated_item))
        await updated_item_model.replace()

    async def delete(self, id: ID) -> None:
        item_model = self.model(id=id)
        await item_model.delete()
