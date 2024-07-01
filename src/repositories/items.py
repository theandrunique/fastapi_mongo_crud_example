from uuid import UUID

from src.items.dto import ItemDTO
from src.items.models import ItemODM, ItemORM
from src.repositories.base.items import ItemsRepository
from src.repositories.base.mongo_repository import MongoDBRepository
from src.repositories.base.sqlalchemy_repository import SQLAlchemyRepository


class MongoItemsRepository(MongoDBRepository[ItemODM, ItemDTO, UUID], ItemsRepository):
    model = ItemODM
    schema = ItemDTO


class SQLAlchemyItemsRepository(
    SQLAlchemyRepository[ItemORM, ItemDTO, UUID],
    ItemsRepository,
):
    model = ItemORM
    schema = ItemDTO
