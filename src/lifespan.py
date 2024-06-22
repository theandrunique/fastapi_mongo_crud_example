from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import settings
from src.container import init_mongodb
from src.database import DatabaseHelper
from src.models import Base


async def on_startup(app: FastAPI) -> None:
    db = DatabaseHelper(url=str(settings.SQLALCHEMY_DATABASE_URL))
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await init_mongodb()


async def on_shutdown(app: FastAPI) -> None: ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await on_startup(app)
    yield
    await on_shutdown(app)
