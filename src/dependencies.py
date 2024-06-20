from fastapi import params

from src.container import container
from src.items.service import ItemsService


def Provide[T](
    dependency: type[T],
) -> T:
    def _dependency():
        return container.resolve(dependency)

    return params.Depends(dependency=_dependency, use_cache=True)  # type: ignore


class Container:
    ItemsService = ItemsService
