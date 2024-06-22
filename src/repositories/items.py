from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.items.models import Item, ItemModel, ItemMongoModel
from src.repositories.base.items import ItemsRepository


class MongoItemsRepository(ItemsRepository):
    async def add(
        self,
        name: str,
        price: float,
        count: int,
    ) -> Item:
        new_item = ItemMongoModel(name=name, price=price, count=count)
        await new_item.insert()
        return Item(
            id=new_item.id,
            name=new_item.name,
            price=new_item.price,
            count=new_item.count,
        )

    async def get(self, id: UUID) -> Item | None:
        item_model = await ItemMongoModel.find_one(ItemMongoModel.id == id)
        if item_model is not None:
            return Item(**item_model.model_dump())

        return None

    async def get_many(self, count: int, offset: int) -> list[Item]:
        result = await ItemMongoModel.find_many().skip(offset).to_list(length=count)
        return [Item(**item.model_dump()) for item in result]

    async def update(self, id: UUID, updated_item: Item):
        item = await ItemMongoModel.find_one(ItemMongoModel.id == id)
        if not item:
            return None
        await item.set(
            {
                "name": updated_item.name,
                "price": updated_item.price,
                "count": updated_item.count,
            }
        )
        return item

    async def delete(self, id: UUID) -> bool:
        item = await ItemMongoModel.find_one(ItemMongoModel.id == id)
        if not item:
            return False

        await item.delete()
        return True


@dataclass(kw_only=True)
class SQLalchemyItemsRepository(ItemsRepository):
    session_maker: async_sessionmaker[AsyncSession]

    async def add(
        self,
        name: str,
        price: float,
        count: int,
    ) -> Item:
        async with self.session_maker() as session:
            new_item = ItemModel(name=name, price=price, count=count)
            session.add(new_item)
            await session.commit()

        return Item(
            id=new_item.id,
            name=new_item.name,
            price=new_item.price,
            count=new_item.count,
        )

    async def get(self, id: UUID) -> Item | None:
        async with self.session_maker() as session:
            item = await session.get(ItemModel, id)

        if item is None:
            return None
        return Item(id=item.id, name=item.name, price=item.price, count=item.count)

    async def get_many(self, count: int, offset: int) -> list[Item]:
        stmt = select(ItemModel).offset(offset).limit(count)

        async with self.session_maker() as session:
            result = await session.execute(stmt)

        return [
            Item(id=item.id, name=item.name, price=item.price, count=item.count)
            for item in result.scalars().all()
        ]

    async def update(self, id: UUID, updated_item: Item):
        async with self.session_maker() as session:
            item = await session.get(ItemModel, id)

            if item is None:
                return

            item.name = updated_item.name
            item.price = updated_item.price
            item.count = updated_item.count
            await session.commit()

    async def delete(self, id: UUID) -> bool:
        async with self.session_maker() as session:
            item = await session.get(ItemModel, id)
            if item is None:
                return False

            await session.delete(item)
            await session.commit()
            return True
