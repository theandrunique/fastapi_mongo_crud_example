from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.items.models import ItemODM, ItemORM, ItemSchema
from src.repositories.base.base_mongo_repository import BaseMongoDBRepository
from src.repositories.base.base_sqlalchemy_repository import BaseSQLAlchemyRepository
from src.repositories.base.items import ItemsRepository


class MongoItemsRepository(BaseMongoDBRepository, ItemsRepository):
    def __init__(self) -> None:
        super().__init__(ItemODM, ItemSchema)


class SQLAlchemyItemsRepository(
    BaseSQLAlchemyRepository[ItemORM, ItemSchema, UUID],
    ItemsRepository,
):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ItemORM, ItemSchema)
