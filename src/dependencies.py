from fastapi import params

from src.container import container
from src.database import Database
from src.items.service import ItemsService
from src.repositories.base.sqlalchemy_repository import SQLAlchemyRepository


def Provide[T](
    dependency: type[T],
) -> T:
    if not container.registrations[dependency]:
        raise ValueError(f"Dependency {dependency} is not registered")

    async def _dependency():
        dep = container.resolve(dependency)

        if hasattr(dep, "repository") and isinstance(
            dep.repository, SQLAlchemyRepository # type: ignore
        ):
            repository: SQLAlchemyRepository = dep.repository  # type: ignore
            db: Database = container.resolve(Database)  # type: ignore
            async with db.session_factory() as session:
                await repository.init(session)
                yield dep
        else:
            yield dep

    return params.Depends(dependency=_dependency, use_cache=True)  # type: ignore


class Container:
    ItemsService = ItemsService
