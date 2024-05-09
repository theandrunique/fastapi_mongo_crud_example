from typing import Annotated

from fastapi import Depends

from src.mongo.client import db

from .repository import ItemsRepository
from .service import ItemsService


async def get_service() -> ItemsService:
    return ItemsService(repository=ItemsRepository(collection=db["items"]))


ItemsServiceDep = Annotated[ItemsService, Depends(get_service)]
