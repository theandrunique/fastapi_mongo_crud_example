from typing import Any

from fastapi import FastAPI

from src.mongo import mongodb_info, ping_mongo


async def on_startup(app: FastAPI) -> None:
    await ping_mongo()
    await mongodb_info()


async def on_shutdown(app: FastAPI) -> None: ...


async def lifespan(app: FastAPI) -> Any:
    await on_startup(app)
    yield
    await on_shutdown(app)
