from uuid import UUID

from src.items.models import ItemODM, ItemORM, ItemSchema
from src.repositories.base.items import ItemsRepository
from src.repositories.base.mongo_repository import MongoDBRepository
from src.repositories.base.sqlalchemy_repository import SQLAlchemyRepository


class MongoItemsRepository(
    MongoDBRepository[ItemODM, ItemSchema, UUID], ItemsRepository
):
    model = ItemODM
    schema = ItemSchema


class SQLAlchemyItemsRepository(
    SQLAlchemyRepository[ItemORM, ItemSchema, UUID],
    ItemsRepository,
):
    model = ItemORM
    schema = ItemSchema
