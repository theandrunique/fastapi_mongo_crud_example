from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClientSession

from .client import client


async def mongo_session() -> AsyncGenerator[AsyncIOMotorClientSession]:
    session = await client.start_session()
    yield session
    session.end_session()


MongoSession = Annotated[AsyncIOMotorClientSession, Depends(mongo_session)]
