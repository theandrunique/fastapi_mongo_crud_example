from fastapi import params

from src.container import container
from src.items.service import ItemsService


def Provide[T](
    dependency: type[T],
) -> T:
    # TODO: add checking if dependency is registered

    async def _dependency():
        dep = container.resolve(dependency)
        return dep

    return params.Depends(dependency=_dependency, use_cache=True)  # type: ignore


class Container:
    ItemsService = ItemsService
