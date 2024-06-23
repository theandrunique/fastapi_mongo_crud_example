from typing import Annotated

from fastapi import Depends, params
from sqlalchemy.ext.asyncio import AsyncSession

from src.container import container
from src.database import DatabaseHelper
from src.items.service import ItemsService


async def get_session() -> AsyncSession:
    db = container.resolve(DatabaseHelper)
    async with db.session_factory() as session:
        yield session


def Provide[T](
    dependency: type[T],
) -> T:
    # TODO: add checking if dependency is registered

    async def _dependency(session: Annotated[AsyncSession, Depends(get_session)]):
        dep = container.resolve(dependency, session=session)
        return dep

    return params.Depends(dependency=_dependency, use_cache=True)  # type: ignore


class Container:
    ItemsService = ItemsService
