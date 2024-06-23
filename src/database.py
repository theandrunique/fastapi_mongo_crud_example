from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


@dataclass(kw_only=True)
class Database:
    session_factory: async_sessionmaker
    engine: AsyncEngine
