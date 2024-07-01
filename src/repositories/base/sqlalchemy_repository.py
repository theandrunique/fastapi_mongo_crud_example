from dataclasses import asdict, dataclass, field

from sqlalchemy import delete, func, select, update

from src.database import DBHelper
from src.dto import BaseDTO
from src.models import BaseORM
from src.repositories.base.repository import Repository


@dataclass
class SQLAlchemyRepository[Model: BaseORM, DTO: BaseDTO, ID](Repository):
    db_helper: DBHelper
    model: type[Model] = field(init=False)
    schema: type[DTO] = field(init=False)

    async def add(self, **kwargs) -> DTO:
        async with self.db_helper.session() as session:
            new_item = self.model(**kwargs)
            session.add(new_item)
            await session.commit()
            return self.schema.from_orm(new_item)

    async def get(self, id: ID) -> DTO | None:
        async with self.db_helper.session() as session:
            item = await session.get(self.model, id)
            if item is None:
                return None
            return self.schema.from_orm(item)

    async def get_many(self, count: int, offset: int) -> list[DTO]:
        async with self.db_helper.session() as session:
            stmt = select(self.model).offset(offset).limit(count)

            result = await session.execute(stmt)
            return [self.schema.from_orm(item) for item in result.scalars().all()]

    async def count(self) -> int:
        async with self.db_helper.session() as session:
            stmt = select(func.count(1)).select_from(self.model)
            result = await session.execute(stmt)
            total_count = result.scalar()
            assert total_count is not None
            return total_count

    async def update(self, id: ID, updated_item: DTO) -> None:
        async with self.db_helper.session() as session:
            stmt = (
                update(self.model)
                .where(self.model.id == id)
                .values(asdict(updated_item))
            )
            await session.execute(stmt)
            await session.commit()

    async def delete(self, id: ID) -> None:
        async with self.db_helper.session() as session:
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
