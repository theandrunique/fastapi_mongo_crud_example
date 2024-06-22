import punq
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.config import settings
from src.database import DatabaseHelper
from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository
from src.repositories.items import SQLalchemyItemsRepository


def init_mongodb() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(
        settings.MONGO_URI.unicode_string(),
        uuidRepresentation="standard",
    )
    return client[settings.MONGO_DATABASE_NAME]


def init_db() -> DatabaseHelper:
    return DatabaseHelper(url=str(settings.SQLALCHEMY_DATABASE_URL))


def init_container() -> punq.Container:
    container = punq.Container()

    monogdb = init_mongodb()

    db_helper = init_db()

    container.register(
        async_sessionmaker[AsyncSession],
        instance=db_helper.session_factory,
        scope=punq.Scope.singleton,
    )

    container.register(
        ItemsRepository, SQLalchemyItemsRepository, scope=punq.Scope.singleton
    )

    container.register(ItemsService, scope=punq.Scope.transient)

    return container


container = init_container()
