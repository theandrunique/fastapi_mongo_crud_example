from typing import Annotated

from fastapi import Depends

from src.mongo import MongoSession

from .repository import ItemRepository


async def get_repository(session: MongoSession) -> ItemRepository:
    return ItemRepository(session=session)


Repository = Annotated[ItemRepository, Depends(get_repository)]
