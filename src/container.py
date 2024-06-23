import punq
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.config import settings
from src.database import DatabaseHelper
from src.items.models import ItemMongoModel
from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository
from src.repositories.items import SQLAlchemyItemsRepository


async def init_mongodb() -> None:
    client = AsyncIOMotorClient(
        settings.MONGO_URI.unicode_string(),
        uuidRepresentation="standard",
    )
    db = client[settings.MONGO_DATABASE_NAME]
    await init_beanie(database=db, document_models=[ItemMongoModel])


def init_db() -> DatabaseHelper:
    return DatabaseHelper(url=str(settings.SQLALCHEMY_DATABASE_URL))


def init_container() -> punq.Container:
    container = punq.Container()

    db_helper = init_db()

    container.register(
        DatabaseHelper,
        instance=db_helper,
        scope=punq.Scope.singleton,
    )

    container.register(
        ItemsRepository, SQLAlchemyItemsRepository, scope=punq.Scope.transient
    )

    # container.register(
        # ItemsRepository, MongoItemsRepository, scope=punq.Scope.singleton
    # )

    container.register(ItemsService, scope=punq.Scope.transient)

    return container


container = init_container()
