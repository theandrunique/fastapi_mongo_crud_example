from dataclasses import dataclass

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseORM


@dataclass
class BaseSQLAlchemyRepository[ModelType: BaseORM, SchemaType: BaseModel, IDType]:
    session: AsyncSession
    model: type[ModelType]
    schema: type[SchemaType]

    async def add(self, **kwargs) -> SchemaType:
        new_item = self.model(**kwargs)
        self.session.add(new_item)
        await self.session.commit()
        return self.schema.model_validate(new_item, from_attributes=True)

    async def get(self, id: IDType) -> SchemaType | None:
        item = await self.session.get(self.model, id)
        if item is None:
            return None
        return self.schema.model_validate(item, from_attributes=True)

    async def get_many(self, count: int, offset: int) -> list[SchemaType]:
        stmt = select(self.model).offset(offset).limit(count)
        result = await self.session.execute(stmt)
        return [
            self.schema.model_validate(item, from_attributes=True)
            for item in result.scalars().all()
        ]

    async def update(self, id: IDType, updated_item: SchemaType):
        item = await self.session.get(self.model, id)
        if item is None:
            return None
        for key, value in updated_item.model_dump().items():
            setattr(item, key, value)
        await self.session.commit()

    async def delete(self, id: IDType) -> bool:
        item = await self.session.get(self.model, id)
        if item is None:
            return False
        await self.session.delete(item)
        await self.session.commit()
        return True
