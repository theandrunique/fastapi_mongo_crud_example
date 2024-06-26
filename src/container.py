import punq
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings
from src.database import DBHelper
from src.items.models import ItemODM
from src.items.service import ItemsService
from src.repositories.base.items import ItemsRepository
from src.repositories.items import SQLAlchemyItemsRepository


async def init_mongodb() -> None:
    client = AsyncIOMotorClient(
        settings.MONGO_URI.unicode_string(),
        uuidRepresentation="standard",
    )
    db = client[settings.MONGO_DATABASE_NAME]
    await init_beanie(database=db, document_models=[ItemODM])


def init_db() -> DBHelper:
    engine = create_async_engine(url=settings.SQLALCHEMY_DATABASE_URL)
    return DBHelper(
        engine=engine,
        session_factory=async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        ),
    )


def init_container() -> punq.Container:
    container = punq.Container()

    container.register(
        DBHelper,
        instance=init_db(),
        scope=punq.Scope.singleton,
    )

    container.register(
        ItemsRepository, SQLAlchemyItemsRepository, scope=punq.Scope.singleton
    )

    # container.register(
    # ItemsRepository, MongoItemsRepository, scope=punq.Scope.singleton
    # )

    container.register(ItemsService, scope=punq.Scope.singleton)

    return container


container = init_container()
