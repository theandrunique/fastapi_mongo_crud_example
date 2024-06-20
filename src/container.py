import punq
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.config import settings
from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository
from src.repositories.items import MongoItemsRepository


def init_mongodb() -> AsyncIOMotorDatabase:
    client = AsyncIOMotorClient(
        settings.MONGO_URI.unicode_string(),
        uuidRepresentation="standard",
    )
    return client[settings.MONGO_DATABASE_NAME]


def init_container() -> punq.Container:
    container = punq.Container()

    monogdb = init_mongodb()

    container.register(
        ItemsRepository,
        instance=MongoItemsRepository(collection=monogdb["items"]),
        scope=punq.Scope.singleton,
    )

    container.register(ItemsService, scope=punq.Scope.singleton)

    return container


container = init_container()
