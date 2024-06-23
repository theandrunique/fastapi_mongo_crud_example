from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.items.models import ItemODM, ItemORM, ItemSchema
from src.repositories.base.items import ItemsRepository


class MongoItemsRepository(ItemsRepository):
    async def add(
        self,
        name: str,
        price: float,
        count: int,
    ) -> ItemSchema:
        new_item = ItemODM(name=name, price=price, item_count=count)
        await new_item.insert()
        return ItemSchema(
            id=new_item.id,
            name=new_item.name,
            price=new_item.price,
            count=new_item.item_count,
        )

    async def get(self, id: UUID) -> ItemSchema | None:
        item_model = await ItemODM.find_one(ItemODM.id == id)
        if item_model is not None:
            return ItemSchema(**item_model.model_dump())

        return None

    async def get_many(self, count: int, offset: int) -> list[ItemSchema]:
        result = await ItemODM.find_many().skip(offset).to_list(length=count)
        return [ItemSchema(**item.model_dump()) for item in result]

    async def update(self, id: UUID, updated_item: ItemSchema):
        item = await ItemODM.find_one(ItemODM.id == id)
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
        item = await ItemODM.find_one(ItemODM.id == id)
        if not item:
            return False

        await item.delete()
        return True


@dataclass
class SQLAlchemyItemsRepository(ItemsRepository):
    session: AsyncSession

    async def add(
        self,
        name: str,
        price: float,
        count: int,
    ) -> ItemSchema:
        new_item = ItemORM(name=name, price=price, count=count)
        self.session.add(new_item)
        await self.session.commit()

        return ItemSchema(
            id=new_item.id,
            name=new_item.name,
            price=new_item.price,
            count=new_item.count,
        )

    async def get(self, id: UUID) -> ItemSchema | None:
        item = await self.session.get(ItemORM, id)

        if item is None:
            return None
        return ItemSchema(
            id=item.id, name=item.name, price=item.price, count=item.count
        )

    async def get_many(self, count: int, offset: int) -> list[ItemSchema]:
        stmt = select(ItemORM).offset(offset).limit(count)

        result = await self.session.execute(stmt)

        return [
            ItemSchema(id=item.id, name=item.name, price=item.price, count=item.count)
            for item in result.scalars().all()
        ]

    async def update(self, id: UUID, updated_item: ItemSchema):
        item = await self.session.get(ItemORM, id)

        if item is None:
            return

        item.name = updated_item.name
        item.price = updated_item.price
        item.count = updated_item.count
        await self.session.commit()

    async def delete(self, id: UUID) -> bool:
        item = await self.session.get(ItemORM, id)
        if item is None:
            return False

        await self.session.delete(item)
        await self.session.commit()
        return True
