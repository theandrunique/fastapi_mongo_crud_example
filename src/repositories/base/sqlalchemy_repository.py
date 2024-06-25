from abc import ABC
from dataclasses import dataclass, field

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import BaseORM


@dataclass
class SQLAlchemyRepository[ModelType: BaseORM, SchemaType: BaseModel, IDType](ABC):
    model: type[ModelType]
    schema: type[SchemaType]
    session: AsyncSession = field(init=False)

    async def init(self, session: AsyncSession):
        self.session = session

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

    async def get_many(self, count: int, offset: int) -> tuple[list[SchemaType], int]:
        stmt = select(self.model).offset(offset).limit(count)
        total_items_stmt = select(func.count(1)).select_from(self.model)
        total_items_result = await self.session.execute(total_items_stmt)
        total_items = total_items_result.scalar()

        result = await self.session.execute(stmt)
        return [
            self.schema.model_validate(item, from_attributes=True)
            for item in result.scalars().all()
        ], total_items  # type: ignore

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
