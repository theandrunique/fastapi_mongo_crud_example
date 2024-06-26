from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.container import container, init_mongodb
from src.database import DBHelper
from src.models import BaseORM


async def on_startup(app: FastAPI) -> None:
    db: DBHelper = container.resolve(DBHelper)  # type: ignore
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)

    await init_mongodb()


async def on_shutdown(app: FastAPI) -> None: ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await on_startup(app)
    yield
    await on_shutdown(app)
