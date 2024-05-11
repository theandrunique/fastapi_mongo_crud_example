from typing import Annotated

from fastapi import Depends

from src.mongo.client import db

from .repository import ItemsRepository
from .service import ItemsService

service = ItemsService(
    repository=ItemsRepository(collection=db["items"]),
)


async def get_service() -> ItemsService:
    return service


ItemsServiceDep = Annotated[ItemsService, Depends(get_service)]
