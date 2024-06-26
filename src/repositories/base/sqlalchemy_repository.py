from dataclasses import dataclass, field

from pydantic import BaseModel
from sqlalchemy import delete, func, select, update

from src.database import DBHelper
from src.models import BaseORM
from src.repositories.base.repository import Repository


@dataclass
class SQLAlchemyRepository[ModelType: BaseORM, SchemaType: BaseModel, IDType](
    Repository
):
    db_helper: DBHelper
    model: type[ModelType] = field(init=False)
    schema: type[SchemaType] = field(init=False)

    async def add(self, **kwargs) -> SchemaType:
        async with self.db_helper.session() as session:
            new_item = self.model(**kwargs)
            session.add(new_item)
            await session.commit()
            return self.schema.model_validate(new_item, from_attributes=True)

    async def get(self, id: IDType) -> SchemaType | None:
        async with self.db_helper.session() as session:
            item = await session.get(self.model, id)
            if item is None:
                return None
            return self.schema.model_validate(item, from_attributes=True)

    async def get_many(self, count: int, offset: int) -> list[SchemaType]:
        async with self.db_helper.session() as session:
            stmt = select(self.model).offset(offset).limit(count)

            result = await session.execute(stmt)
            return [
                self.schema.model_validate(item, from_attributes=True)
                for item in result.scalars().all()
            ]

    async def count(self) -> int:
        async with self.db_helper.session() as session:
            stmt = select(func.count(1)).select_from(self.model)
            result = await session.execute(stmt)
            total_count = result.scalar()
            assert total_count is not None
            return total_count

    async def update(self, id: IDType, updated_item: SchemaType) -> None:
        async with self.db_helper.session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(**updated_item.model_dump())
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, id: IDType) -> None:
        async with self.db_helper.session() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
