from typing import Any

from fastapi import FastAPI

from src.mongo import test_connection


async def on_startup(app: FastAPI) -> None:
    await test_connection()
    ...

async def on_shutdown(app: FastAPI) -> None:
    ...

async def lifespan(app: FastAPI) -> Any:
    await on_startup(app)
    yield
    await on_shutdown(app)
